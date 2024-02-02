"""
Automatically generated file from a JSON schema.
"""

from typing import Any, Literal, TypedDict, Union

CORE_SCHEMA_META_SCHEMA_DEFAULT = True
""" Default value of the field path 'JSONSchema' """


JSONSchema = Union["JSONSchemaItem", bool]
"""
Core schema meta-schema.

default: True
"""


# default: True
JSONSchemaItem = TypedDict(
    "JSONSchemaItem",
    {
        # format: uri-reference
        "$id": str,
        # format: uri
        "$schema": str,
        # format: uri-reference
        "$ref": str,
        "$comment": str,
        "title": str,
        "description": str,
        "default": Any,
        # default: False
        "readOnly": bool,
        # default: False
        "writeOnly": bool,
        "examples": list[Any],
        # exclusiveMinimum: 0
        "multipleOf": Union[int, float],
        "maximum": Union[int, float],
        "exclusiveMaximum": Union[int, float],
        "minimum": Union[int, float],
        "exclusiveMinimum": Union[int, float],
        # minimum: 0
        "maxLength": "_NonNegativeInteger",
        # minimum: 0
        # default: 0
        "minLength": "_NonNegativeIntegerDefault0",
        # format: regex
        "pattern": str,
        # Core schema meta-schema.
        #
        # default: True
        "additionalItems": "JSONSchema",
        # default: True
        #
        # Aggregation type: anyOf
        "items": "_CoreSchemaMetaSchemaObjectItems",
        # minimum: 0
        "maxItems": "_NonNegativeInteger",
        # minimum: 0
        # default: 0
        "minItems": "_NonNegativeIntegerDefault0",
        # default: False
        "uniqueItems": bool,
        # Core schema meta-schema.
        #
        # default: True
        "contains": "JSONSchema",
        # minimum: 0
        "maxProperties": "_NonNegativeInteger",
        # minimum: 0
        # default: 0
        "minProperties": "_NonNegativeIntegerDefault0",
        # uniqueItems: True
        # default:
        #   []
        "required": "_StringArray",
        # Core schema meta-schema.
        #
        # default: True
        "additionalProperties": "JSONSchema",
        # default:
        #   {}
        "definitions": dict[str, "JSONSchema"],
        # default:
        #   {}
        "properties": dict[str, "JSONSchema"],
        # propertyNames:
        #   format: regex
        # default:
        #   {}
        "patternProperties": dict[str, "JSONSchema"],
        "dependencies": dict[str, "_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties"],
        # Core schema meta-schema.
        #
        # default: True
        "propertyNames": "JSONSchema",
        "const": Any,
        # minItems: 1
        # uniqueItems: True
        "enum": list[Any],
        # Aggregation type: anyOf
        "type": "_CoreSchemaMetaSchemaObjectType",
        "format": str,
        "contentMediaType": str,
        "contentEncoding": str,
        # Core schema meta-schema.
        #
        # default: True
        "if": "JSONSchema",
        # Core schema meta-schema.
        #
        # default: True
        "then": "JSONSchema",
        # Core schema meta-schema.
        #
        # default: True
        "else": "JSONSchema",
        # minItems: 1
        "allOf": "_SchemaArray",
        # minItems: 1
        "anyOf": "_SchemaArray",
        # minItems: 1
        "oneOf": "_SchemaArray",
        # Core schema meta-schema.
        #
        # default: True
        "not": "JSONSchema",
    },
    total=False,
)


_CORE_SCHEMA_META_SCHEMA_OBJECT_DEFINITIONS_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object definitions' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_ITEMS_DEFAULT = True
""" Default value of the field path 'Core schema meta-schema object items' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PATTERNPROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object patternProperties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_PROPERTIES_DEFAULT: dict[str, Any] = {}
""" Default value of the field path 'Core schema meta-schema object properties' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_READONLY_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object readOnly' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_UNIQUEITEMS_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object uniqueItems' """


_CORE_SCHEMA_META_SCHEMA_OBJECT_WRITEONLY_DEFAULT = False
""" Default value of the field path 'Core schema meta-schema object writeOnly' """


_CoreSchemaMetaSchemaObjectDependenciesAdditionalproperties = Union["JSONSchema", "_StringArray"]
""" Aggregation type: anyOf """


_CoreSchemaMetaSchemaObjectItems = Union["JSONSchema", "_SchemaArray"]
"""
default: True

Aggregation type: anyOf
"""


_CoreSchemaMetaSchemaObjectType = Union["_SimpleTypes", "_CoreSchemaMetaSchemaObjectTypeAnyof1"]
""" Aggregation type: anyOf """


_CoreSchemaMetaSchemaObjectTypeAnyof1 = list["_SimpleTypes"]
"""
minItems: 1
uniqueItems: True
"""


_NON_NEGATIVE_INTEGER_DEFAULT0_DEFAULT = 0
""" Default value of the field path 'non negative integer default0' """


_NonNegativeInteger = int
""" minimum: 0 """


_NonNegativeIntegerDefault0 = int
"""
minimum: 0
default: 0
"""


_STRING_ARRAY_DEFAULT: list[Any] = []
""" Default value of the field path 'string array' """


_SchemaArray = list["JSONSchema"]
""" minItems: 1 """


_SimpleTypes = Union[
    Literal["array"],
    Literal["boolean"],
    Literal["integer"],
    Literal["null"],
    Literal["number"],
    Literal["object"],
    Literal["string"],
]
_SIMPLETYPES_ARRAY: Literal["array"] = "array"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_BOOLEAN: Literal["boolean"] = "boolean"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_INTEGER: Literal["integer"] = "integer"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NULL: Literal["null"] = "null"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_NUMBER: Literal["number"] = "number"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_OBJECT: Literal["object"] = "object"
"""The values for the '_SimpleTypes' enum"""
_SIMPLETYPES_STRING: Literal["string"] = "string"
"""The values for the '_SimpleTypes' enum"""


_StringArray = list[str]
"""
uniqueItems: True
default:
  []
"""
