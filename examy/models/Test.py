import dataclasses


@dataclasses.dataclass(frozen=True)
class Test:
    """Describe a test in an exam."""
    name: str
    """Name of the test."""
    short_name: str
    """Short name of the test.
    
    It must be unique among all tests in the exam."""
    question_count: int
    """Question count of the test."""
