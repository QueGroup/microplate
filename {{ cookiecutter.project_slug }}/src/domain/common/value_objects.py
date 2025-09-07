import abc
import dataclasses


@dataclasses.dataclass(frozen=True)
class BaseValueObject(abc.ABC):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Check that a value is valid to create this value object"""
        pass


@dataclasses.dataclass(frozen=True)
class ValueObject[V](BaseValueObject, abc.ABC):
    value: V

    def to_raw(self) -> V:
        return self.value
