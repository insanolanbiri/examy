import dataclasses

from examy.models.Test import Test


@dataclasses.dataclass(frozen=True)
class TestResult:
    net: float
    true_count: int
    false_count: int
    test: dataclasses.InitVar[Test]
    _empty_count: dataclasses.InitVar[int] = None
    empty_count: int = dataclasses.field(init=False)

    def __post_init__(self, test, _empty_count):
        if _empty_count is None:
            _empty_count = test.question_count - self.true_count - self.false_count
        object.__setattr__(self, "empty_count", _empty_count)
