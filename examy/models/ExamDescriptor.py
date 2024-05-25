import dataclasses

from examy.models.Test import Test


@dataclasses.dataclass(frozen=True)
class ExamDescriptor:
    login_url: str
    result_page_layout: str
    exam_name: str
    friendly_name: str
    tests: list[Test]
    logout_url: str = None
