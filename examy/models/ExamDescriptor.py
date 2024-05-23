import dataclasses

from examy.models.TestDescriptor import TestDescriptor


@dataclasses.dataclass(frozen=True)
class ExamDescriptor:
    login_url: str
    result_page_layout: str
    exam_name: str
    test_descriptors: list[TestDescriptor]
    logout_url: str = None
