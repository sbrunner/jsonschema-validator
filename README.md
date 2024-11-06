# JSON Schema validator

Tools to generate Python types based on TypedDict from a JSON schema

## Quick start

install:

```bash
python3 -m pip install --user jsonschema-validator-new
```

Convert a JSON schema to a Python file contains the types:

```bash
jsonschema-validator --help
```

## Default

The default values are exported in the Python file, then you can do something like that:

```python
value_with_default = my_object.get('field_name', my_schema.FIELD_DEFAULT)
```

## Validation

This package also provide some validations features for YAML file based on `jsonschema`.

Additional features:

- Obtain the line and columns number in the errors, if the file is loaded with `ruamel.yaml`.
- Export the default provided in the JSON schema.

```python
import ruamel.yaml
import pkgutil
import jsonschema_validator
import json

schema_data = pkgutil.get_data("<package>", "schema.json")
schema = json.loads(jsonschema_validator)
with open(filename) as data_file:
    yaml = ruamel.yaml.YAML()  # type: ignore
    data = yaml.load(data_file)
errors, _ = jsonschema_validator.validate(filename, data, schema)
if errors:
    print("\n".join(errors))
    sys.exit(1)
```

## Pre-commit hooks

This project provides pre-commit hooks to automatically generate the files.

```yaml
repos:
  - repo: https://github.com/camptocamp/jsonschema-validator
    rev: <version> # Use the ref you want to point at
    hools:
      - id: jsonschema-validator
        files: |
          (?x)^(
              ...
          )$
```

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```

The `prospector` tests should pass.

The code should be typed.

The code should be tested with `pytests`.
