import dataclasses


@dataclasses.dataclass(frozen=True)
class Test:
    name: str
    short_name: str
    question_count: int
