import copy
from drf_yasg.inspectors import SwaggerAutoSchema

from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_overrides(self, view, method):
        """Get overrides specified for a given operation.

        :param view: the view associated with the operation
        :param str method: HTTP method
        :return: a dictionary containing any overrides set by :func:`@swagger_auto_schema <.swagger_auto_schema>`
        :rtype: dict
        """
        method = method.lower()
        action = getattr(view, "action", method)
        action_method = getattr(view, action, None)
        overrides = getattr(action_method, "_swagger_auto_schema", {})
        if method in overrides:  # noqa
            overrides = overrides[method]
        tags = getattr(view, "tags", None)
        if tags:
            overrides["tags"] = tags

        return copy.deepcopy(overrides)


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys):
        """
        Generate an operation ID based on the model, HTTP method, and other keys.
        """

        # If operation_id is explicitly provided, use it.
        operation_id = self.overrides.get('operation_id', '')
        if operation_id:
            return operation_id

        model_name = self._get_model_name()

        # Get the action from operation_keys.
        action = operation_keys[-1].replace("_", " ")

        # Get the subtag, if it exists.
        subtag = getattr(self.view, 'subtag', '')
        formatted_subtag = f"[{subtag}]" if subtag else ""

        # Construct the operation ID.
        return f"{formatted_subtag}  {model_name} {action}"

    def _get_model_name(self):
        """
        Derive the model name from the view.
        """
        # Directly get from model_name if available.
        if hasattr(self.view, "model_name"):
            return self.view.model_name

        # If a serializer is defined and it has a Meta class, derive the model name.
        if getattr(self.view, "serializer_class", None):
            serializer = self.view.get_serializer()
            if hasattr(serializer, "Meta") and hasattr(serializer.Meta, "model"):
                return serializer.Meta.model.__name__

        # If the view has a queryset, derive the model name from it.
        if hasattr(self.view, "get_queryset"):
            queryset = self.view.get_queryset()
            if queryset:
                return queryset.model.__name__

        return ""
