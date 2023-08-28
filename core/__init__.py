from flask_apispec.apidoc import Converter
from funcy import first, project
import copy
from marshmallow import Schema
from flask import current_app
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from typing import Optional


class ApiDocConverter(Converter):
    def get_operation(self, rule, view, parent=None):
        from flask_apispec.utils import resolve_annotations, merge_recursive

        annotation = resolve_annotations(view, "docs", parent)
        docs = merge_recursive(annotation.options)
        operation = {
            "responses": self.get_responses(view, parent),
            "parameters": self.get_parameters(rule, view, docs, parent),
        }
        request_body = self.get_request_body(view, parent)
        if request_body:
            operation["requestBody"] = request_body
        docs.pop("params", None)
        return merge_recursive([operation, docs])

    def get_responses(self, view, parent=None):
        response = super().get_responses(view, parent)

        for status_code in response:
            result = {}
            result['description'] = response[status_code]['description']
            result['content'] = {}
            result['content']['application/json'] = {'schema': response[status_code]['schema']}
            response[status_code] = result
        return response

    def get_parameters(self, rule, view, docs, parent=None):
        parameters = super().get_parameters(rule, view, docs)
        return [parameter for parameter in parameters if parameter["in"] != "body"]

    def get_request_body(self, view, parent=None):
        schema, locations, options = self._parse_args_annotation(view, parent)
        converter = self._resolve_converter(schema)

        if schema is None:
            return None

        # if not locations or not any(location in ("json", "form", "files") for location in locations):
        #     return None
        if not locations:
            return None

        options = dict(options)
        options["default_in"] = "body"
        params = converter(schema, **options)
        param = first(params)
        if param is None:
            return None

        result = project(param, ["description", "required"])
        result["content"] = {}
        for location in locations.keys():
            if "json" == locations[location][0]:
                result["content"]["application/json"] = {"schema": param["schema"]}
            elif "form" == locations[location]:
                result["content"]["application/x-www-form-urlencoded"] = {"schema": param["schema"]}
            elif "files" == locations[location]:
                result["content"]["multipart/form-data"] = {"schema": param["schema"]}
        if not result["content"]:
            return None
        return result

    def _parse_args_annotation(self, view, parent=None):
        from flask_apispec.utils import resolve_annotations

        annotation = resolve_annotations(view, "args", parent)
        args = first(annotation.options)
        if not args or "args" not in args:
            return None, None, None

        schema = args["args"]
        options = copy.copy(args.get("kwargs", {}))
        locations = options.pop("location", [])
        return schema, options, locations

    def _resolve_converter(self, schema):
        from marshmallow.utils import is_instance_or_subclass

        openapi = self.marshmallow_plugin.converter

        if is_instance_or_subclass(schema, Schema):
            return openapi.schema2parameters

        if callable(schema):
            schema = schema(request=None)
            if is_instance_or_subclass(schema, Schema):
                return openapi.schema2parameters

        return openapi.fields2jsonschema


def _get_bp_name(endpoint: str) -> Optional[str]:
    splitted = endpoint.split(".")
    if len(splitted) > 1:
        return splitted[0]
    return None


def generate_api_spec(title=None, version=None, bp_name=None, global_params=None) -> dict:
    from flask_apispec.paths import rule_to_path
    from config import DevelopConfig
    # Config 정리시 수정 필요
    spec = DevelopConfig.APISPEC_SPEC

    converter = ApiDocConverter(current_app, spec)

    for endpoint, view_func in current_app.view_functions.items():
        endpoint_bp_name = _get_bp_name(endpoint)
        if endpoint_bp_name != bp_name:
            continue

        print(view_func)
        if hasattr(view_func, "__apispec__"):
            # noinspection PyProtectedMember
            rule = current_app.url_map._rules_by_endpoint[endpoint][0]
            spec.path(
                view=view_func,
                path=rule_to_path(rule),
                operations={method.lower(): converter.get_operation(rule, view_func, converter.get_parent(view_func)) for method in rule.methods if method not in ["OPTIONS", "HEAD"]},
                parameters=global_params,
            )

    return spec.to_dict()
