import pytest
import ruamel.yaml
import yaml

import jsonschema_validator


def test_validate_ruamel():
    ruamel_yaml = ruamel.yaml.YAML()
    errors, data = jsonschema_validator.validate(
        "test.yaml",
        ruamel_yaml.load(
            """
root:
  - 8
  - test: 8
  - toto: 8"""
        ),
        {
            "type": "object",
            "properties": {
                "root": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"test": {"type": "string"}},
                        "required": ["test"],
                    },
                },
            },
        },
    )
    assert errors == [
        "-- test.yaml:3:3 root.0: 8 is not of type 'object' (rule: properties.root.items.type)",
        "-- test.yaml:4:5 root.1.test: 8 is not of type 'string' (rule: properties.root.items.properties.test.type)",
        "-- test.yaml:5:5 root.2: 'test' is a required property (rule: properties.root.items.required)",
    ]


def test_validate_yaml():
    errors, data = jsonschema_validator.validate(
        "test.yaml",
        yaml.load(
            """
root:
  - 8
  - test: 8
  - toto: 8""",
            Loader=yaml.SafeLoader,
        ),
        {
            "type": "object",
            "properties": {
                "root": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"test": {"type": "string"}},
                        "required": ["test"],
                    },
                },
            },
        },
    )
    assert errors == [
        "-- test.yaml root.0: 8 is not of type 'object' (rule: properties.root.items.type)",
        "-- test.yaml root.1.test: 8 is not of type 'string' (rule: properties.root.items.properties.test.type)",
        "-- test.yaml root.2: 'test' is a required property (rule: properties.root.items.required)",
    ]


def test_validate_deep():
    errors, data = jsonschema_validator.validate(
        "test.yaml",
        yaml.load(
            """
root:
  level2:
    test: 8""",
            Loader=yaml.SafeLoader,
        ),
        {
            "type": "object",
            "properties": {
                "root": {
                    "type": "object",
                    "properties": {
                        "level2": {
                            "type": "object",
                            "properties": {
                                "test": {"type": "string"},
                            },
                        }
                    },
                },
            },
        },
    )
    assert errors == [
        "-- test.yaml root.level2.test: 8 is not of type 'string' (rule: properties.root.properties.level2.properties.test.type)",
    ]


def test_default():
    errors, data = jsonschema_validator.validate(
        "test.yaml",
        {},
        {
            "type": "object",
            "properties": {
                "root": {
                    "default": "abc",
                },
            },
        },
        default=True,
    )
    assert data == {"root": "abc"}


def test_command_correct():
    jsonschema_validator.main(["tests/correct.yaml"])


def test_command_wrong():
    with pytest.raises(SystemExit) as result:
        jsonschema_validator.main(["tests/wrong.yaml"])
    assert result.value.code == 1, result.value
