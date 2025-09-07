import dataclasses

from domain.common import AppError


@dataclasses.dataclass(eq=False)
class MissingFieldsError(AppError):
    fields: list[str]

    @property
    def title(self) -> str:
        field_names = ", ".join(self.fields)
        return f"You must specify one of the fields: {field_names}"
