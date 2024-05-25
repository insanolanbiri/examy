from dataclasses import dataclass, InitVar, field
from typing import Iterator

from examy.models.ExamDescriptor import ExamDescriptor
from examy.models.Ranking import Ranking
from examy.models.Test import Test
from examy.models.TestResult import TestResult


@dataclass(frozen=True)
class ExamReport:
    descriptor: ExamDescriptor
    score: float
    _test_results: list[TestResult]
    ranks: Ranking = None
    _true_count: InitVar[int] = None
    _false_count: InitVar[int] = None
    _empty_count: InitVar[int] = None
    _net: InitVar[float] = None
    _question_count: InitVar[int] = None
    true_count: int = field(init=False)
    false_count: int = field(init=False)
    empty_count: int = field(init=False)
    net: float = field(init=False)
    question_count: int = field(init=False)

    def __post_init__(self, _true_count, _false_count, _empty_count, _net, _question_count):
        if _true_count is None:
            _true_count = sum([test.true_count for test in self._test_results])
        object.__setattr__(self, "true_count", _true_count)

        if _false_count is None:
            _false_count = sum([test.false_count for test in self._test_results])
        object.__setattr__(self, "false_count", _false_count)

        if _empty_count is None:
            _empty_count = sum([test.empty_count for test in self._test_results])
        object.__setattr__(self, "empty_count", _empty_count)

        if _net is None:
            _net = sum([test.net for test in self._test_results])
        object.__setattr__(self, "net", _net)

        if _question_count is None:
            _question_count = sum([test_d.question_count for test_d in self.descriptor.tests])
        object.__setattr__(self, "question_count", _question_count)

    def iter_tests(self) -> Iterator[tuple[Test, TestResult]]:
        return zip(self.descriptor.tests, self._test_results)
