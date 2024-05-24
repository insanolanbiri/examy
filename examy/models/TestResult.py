import dataclasses

from examy.models.TestDescriptor import TestDescriptor


@dataclasses.dataclass(frozen=True)
class TestResult:
    net: float
    true_count: int
    false_count: int
    descriptor: dataclasses.InitVar[TestDescriptor]
    _empty_count: dataclasses.InitVar[int] = None
    empty_count: int = dataclasses.field(init=False)

    def __post_init__(self, descriptor, _empty_count):
        if _empty_count is None:
            _empty_count = descriptor.question_count - self.true_count - self.false_count
        object.__setattr__(self, "empty_count", _empty_count)
