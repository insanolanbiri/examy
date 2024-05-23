import dataclasses


@dataclasses.dataclass(frozen=True)
class TestDescriptor:
    name: str
    short_name: str
    question_count: int
