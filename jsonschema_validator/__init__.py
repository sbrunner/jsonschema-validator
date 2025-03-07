"""Module that offer some useful functions to validate the data against a JSON schema."""

import argparse
import json
import logging
import re
import sys
import urllib.parse
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional
from warnings import warn

import jsonschema
import requests
import ruamel.yaml

import jsonschema_validator.json_schema

LOG = logging.getLogger(__name__)


def _extend_with_default(
    validator_class: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
) -> "jsonschema.validators._DefaultTypesDeprecatingMetaClass":
    """
    Add the default provider.

    Extends the jsonschema validator by adding a validator that fill the missing value with the default
    provided by the JSON schema.

    Arguments:
        validator_class: The validator class to be patched
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(
        validator: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
        properties: dict[str, jsonschema_validator.json_schema.JSONSchemaItem],
        instance: Optional[dict[str, Any]],
        schema: jsonschema_validator.json_schema.JSONSchemaItem,
    ) -> Iterator[jsonschema.exceptions.ValidationError]:
        """
        Set the default from the JSON schema to the data.

        Arguments:
            validator: The validator class
            properties: The properties
            instance: The data class
            schema: The full schema
        """
        for prop, subschema in properties.items():
            if "$ref" in subschema:
                ref = subschema["$ref"]
                resolve = getattr(validator.resolver, "resolve", None)
                if resolve is None:
                    with validator.resolver.resolving(ref) as resolved:
                        yield from validator.descend(instance, resolved)
                else:
                    _, resolved = validator.resolver.resolve(ref)
                    subschema = dict(subschema)  # type: ignore[assignment] # noqa: PLW2901
                    subschema.update(resolved)
            if "default" in subschema and instance is not None:
                instance.setdefault(prop, subschema["default"])

        yield from validate_properties(
            validator,
            properties,
            instance,
            schema,
        )

    return jsonschema.validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


def validate(
    filename: str,
    data: dict[str, Any],
    schema: dict[str, Any],
    default: bool = False,
) -> tuple[list[str], dict[str, Any]]:
    """
    Validate the YAML, with it's JSON schema.

    Arguments:
        filename: Name used to generate the error messages
        data: The data structure to be validated (should be loaded with ruamel.yaml to have the lines numbers)
        schema: The loaded JSON schema
        default: If true, fill the data with the defaults provided in the JSON schema, not working as expected
            with AnyOf and OneOf
    """
    schema_ref = schema.get("$schema", "default")
    schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
    Validator = {  # pylint: disable=invalid-name
        "draft-04": jsonschema.Draft4Validator,
        "draft-06": jsonschema.Draft6Validator,
        "draft-07": jsonschema.Draft7Validator,
    }.get(
        schema_match.group(1) if schema_match else "default",
        jsonschema.Draft7Validator,
    )
    if default:
        warn(
            "This is deprecated, use `obj.get('field', schema.FIELD_TYPE_DEFAULT)` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        Validator = _extend_with_default(Validator)  # noqa: N806

    validator = Validator(schema)

    def format_error(error: jsonschema.exceptions.ValidationError) -> list[str]:
        position = filename

        if hasattr(error.instance, "lc"):
            position = f"{filename}:{error.instance.lc.line + 1}:{error.instance.lc.col + 1}"
        else:
            curent_data = data
            parent = None
            if hasattr(curent_data, "lc"):
                parent = curent_data
            for path in error.absolute_path:
                curent_data = curent_data[path]
                if hasattr(curent_data, "lc"):
                    parent = curent_data
            if parent is not None:
                position = f"{filename}:{parent.lc.line + 1}:{parent.lc.col + 1}"

        if error.context:
            results = []
            for context in error.context:
                results += format_error(context)
            return results
        rule = (
            f" (rule: {'.'.join([str(i) for i in error.absolute_schema_path])})"
            if error.absolute_schema_path
            else ""
        )
        return [
            f"-- {position} "
            f"{'.'.join([str(i) for i in error.absolute_path] if error.absolute_path else '/')}: "
            f"{error.message}{rule}",
        ]

    results = []
    for error in validator.iter_errors(data):
        results += format_error(error)
    return sorted(results), data


class ValidationError(Exception):
    """Exception thrown on validation issue."""

    def __init__(self, message: str, data: Any) -> None:
        """
        Construct.

        Arguments:
            message: The error message
            data: The validated data
        """
        super().__init__(message)
        self.data = data


def main(argv: Optional[list[str]] = None) -> None:
    """Check the JSON ort YAML files against the JSON schema files."""
    argparser = argparse.ArgumentParser("Check the JSON or YAML files against the JSON schema files")
    argparser.add_argument("--schema", help="The JSON schema")
    argparser.add_argument("--json", action="store_true", help="Parse as JSON")
    argparser.add_argument("--yaml", action="store_true", help="Parse as YAML")
    argparser.add_argument("--timeout", default=30, type=int, help="Timeout in seconds")
    argparser.add_argument("files", type=Path, nargs="+", help="The files to check")
    args = argparser.parse_args(argv)

    if args.json and args.yaml:
        print("You can not specify both --json and --yaml")
        sys.exit(2)

    schema_re = re.compile(r".*schema=(\S+)")
    yaml = ruamel.yaml.YAML()
    is_json = args.json
    is_yaml = args.yaml
    schema = args.schema

    for file in args.files:
        validate_file(file, schema, yaml, args.timeout, schema_re, is_json=is_json, is_yaml=is_yaml)


def validate_file(
    file: Path,
    schema: Optional[str],
    yaml: ruamel.yaml.YAML,
    timeout: int,
    schema_re: re.Pattern[str],
    is_json: bool,
    is_yaml: bool,
) -> None:
    """Validate the file."""
    has_arg_schema = schema is not None

    if not is_json and not is_yaml:
        is_json = file.suffix == ".json"
        is_yaml = file.suffix in [".yaml", ".yml"]

    if not is_json and not is_yaml:
        print(f"Unknown file type: {file}")
        sys.exit(2)

    if schema is None and is_yaml:
        with file.open(encoding="utf-8") as data_file:
            match = schema_re.match(data_file.readline().strip())
            if match is not None:
                schema = match.group(1)

    data: dict[str, Any] = {}
    if is_yaml:
        with file.open(encoding="utf-8") as data_file:
            data = yaml.load(data_file)
    elif is_json:
        with file.open(encoding="utf-8") as data_file:
            data = json.load(data_file)

    if schema is None:
        schema = data.get("$schema")

    if schema is None:
        print(f"Could not find the schema for {file}")
        sys.exit(2)

    schema_data: dict[str, Any] = {}
    if urllib.parse.urlparse(schema).scheme == "":
        if not has_arg_schema:
            schema_path = file.parent / schema
            schema = str(schema_path)
        else:
            schema_path = Path(schema)
        with schema_path.open(encoding="utf-8") as schema_file:
            schema_data = json.load(schema_file)
    else:
        response = requests.get(schema, timeout=timeout)
        if not response.ok:
            print(f"Could not load the schema {schema}")
            sys.exit(2)

        schema_data = response.json()
    results, _ = validate(str(file), data, schema_data)
    if results:
        print(f"Validation errors in {file}:")
        for result in results:
            print(result)
        sys.exit(1)
