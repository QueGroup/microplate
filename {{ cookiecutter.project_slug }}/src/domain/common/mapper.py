import abc
from typing import Any

from .aggregate_root import AggregateRoot


class IMapper[T_Entity: AggregateRoot, T_Dto: Any](abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def to_dto(entity: T_Entity) -> T_Dto:
        pass
