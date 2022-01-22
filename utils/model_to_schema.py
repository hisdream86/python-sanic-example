from pydantic.main import BaseModel
from sanic_openapi import openapi
from sanic_openapi.openapi3.types import Schema
from typing import Any, Dict, List, Type

_SUPPORTED_ATTRIBUTES = frozenset(["format", "enum", "required", "example"])


def _to_schema(definition_stack: List[str], schema_def: Dict[str, Any], definitions: Dict[str, Any]) -> Schema:
    type = schema_def.get("type")

    if type == "object":
        properties_spec = schema_def.get("properties", {})
        properties = {}
        for key in properties_spec:
            properties[key] = _to_schema(
                definition_stack=definition_stack, schema_def=properties_spec[key], definitions=definitions
            )
        schema = openapi.Object(
            title=schema_def.get("title"),
            description=schema_def.get("description"),
            required=schema_def.get("required"),
            properties=properties,
        )
    elif type == "array":
        schema = openapi.Array(
            description=schema_def.get("description"),
            required=schema_def.get("required"),
            items=_to_schema(
                definition_stack=definition_stack, schema_def=schema_def.get("items"), definitions=definitions
            ),
        )
    elif type is None:
        if allof_spec := schema_def.get("allOf"):  # Model, Enum
            definition = allof_spec[0]["$ref"].split("/")[-1]
            schema = (
                _to_schema(
                    definition_stack=definition_stack + [definition],
                    schema_def={**definitions.get(definition)},
                    # schema_def={**definitions.get(definition), "required": schema_def.get("required", False)},
                    definitions=definitions,
                )
                if definition not in definition_stack
                else openapi.Object(title=definition, description=schema_def.get("description"))
            )

        elif anyof_spec := schema_def.get("anyOf"):  # Union
            anyof = []
            for any in anyof_spec:
                if any.get("type"):
                    schema_type_obj = Schema(**{"type": any.get("type"), "description": any.get("description")})
                    anyof.append(schema_type_obj)
                else:
                    definition = any["$ref"].split("/")[-1]
                    anyof.append(
                        _to_schema(
                            definition_stack=definition_stack + [definition],
                            schema_def=definitions.get(definition),
                            definitions=definitions,
                        )
                        if definition not in definition_stack
                        else anyof.append(
                            openapi.Object(
                                title=definition, description=schema_def.get("description", definition), properties={}
                            )
                        )
                    )
            schema = Schema(anyOf=anyof)
        elif schema_def.get("$ref"):  # $ref
            definition = schema_def.get("$ref").split("/")[-1]
            schema = _to_schema(
                definition_stack=definition_stack, schema_def=definitions.get(definition), definitions=definitions
            )
        else:  # Any type
            schema = Schema(**{"type": "object", "description": schema_def.get("description")})

    else:
        schema_spec = {"type": schema_def.get("type"), "description": schema_def.get("description")}
        for spec in _SUPPORTED_ATTRIBUTES:
            if schema_def.get(spec):
                schema_spec[spec] = schema_def.get(spec)
        schema = Schema(**schema_spec)

    return schema


def model_to_schema(model: Type[BaseModel]) -> Schema:
    schema = model.schema()
    return _to_schema(
        definition_stack=[],
        schema_def=dict(filter(lambda key: key[0] != "definitions", schema.items())),
        definitions=schema.get("definitions"),
    )
