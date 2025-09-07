import dataclasses


@dataclasses.dataclass(eq=False)
class AppError(Exception):
    @property
    def title(self) -> str:
        return "An app error occurred"
