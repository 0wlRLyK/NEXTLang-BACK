from dataclasses import dataclass
from typing import Any, Callable, Optional, Type, Union


@dataclass
class LearningSphereDTO:
    grammar: Optional[Union[Callable, Type]] = None
    vocabulary: Optional[Union[Callable, Type]] = None
    audition: Optional[Union[Callable, Type]] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)
