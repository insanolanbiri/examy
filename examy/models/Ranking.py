import dataclasses
from typing import Sequence


@dataclasses.dataclass(frozen=True)
class Ranking:
    class_rank: int = None
    class_attendance: int = None
    school_rank: int = None
    school_attendance: int = None
    district_rank: int = None
    district_attendance: int = None
    province_rank: int = None
    province_attendance: int = None
    global_rank: int = None
    global_attendance: int = None

    @classmethod
    def from_sequences(cls, ranks: Sequence[int], attendances: Sequence[int]) -> "Ranking":
        assert len(ranks) == len(attendances) == 4
        one_by_one = []

        for pair in zip(ranks, attendances):
            one_by_one.extend(pair)

        return cls(*one_by_one)
