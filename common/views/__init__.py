# type: ignore
from typing import Any, Callable, Optional, Tuple, Type, Union

from rest_framework import mixins
from rest_framework.decorators import action as drf_action
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet, ViewSet


def action_with_serializer(
    *, serializer_class: Optional[Type[Serializer]] = None, **kwargs
) -> Callable:
    def decorator(func: Callable) -> Callable:
        setattr(func, "bound_serializer_class", serializer_class)  # noqa
        return drf_action(**kwargs)(func)

    return decorator


class CustomActionMixin:
    serializer_class: Type[Serializer]
    action: str

    @classmethod
    def custom_action(
        cls, *args: Tuple[Any], **kwargs: Any
    ) -> Callable:  # Renamed to custom_action
        serializer_class = kwargs.pop("serializer_class", None)
        if serializer_class:
            return action_with_serializer(serializer_class=serializer_class, **kwargs)
        return drf_action(*args, **kwargs)

    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer:
        serializer_class = getattr(
            getattr(self, self.action), "bound_serializer_class", None
        )
        if not serializer_class:
            serializer_class = self.serializer_class

        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)  # type: ignore


class CustomViewSet(CustomActionMixin, ViewSet):
    def get_serializer_context(self) -> dict[str, Union[Any, str]]:
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}


class CustomGenericViewSet(GenericViewSet):
    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer:
        serializer_class = getattr(
            getattr(self, self.action), "bound_serializer_class", None
        )
        if not serializer_class:
            serializer_class = self.serializer_class

        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)  # type: ignore


class CustomModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    CustomGenericViewSet,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
