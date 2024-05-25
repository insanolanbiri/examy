import dataclasses

from examy.models.ExamReport import ExamReport


@dataclasses.dataclass
class Student:
    name: str
    number: int
    school: str
    province: str
    district: str
    grade_: dataclasses.InitVar[str | int]
    class_: str
    reports: list[ExamReport] = dataclasses.field(default_factory=list)
    login_name: str = ""
    grade: str = dataclasses.field(init=False)

    def __post_init__(self, grade_):
        """Post init method."""
        if isinstance(grade_, int):
            self.grade = str(grade_) + ".Sınıf"
        else:
            self.grade = grade_

        if not self.login_name:
            self.login_name = self.name.split()[0]

        # fix capitalization
        from examy.utils import TurkishStr

        self.school = TurkishStr.upper(self.school)
        self.district = TurkishStr.upper(self.district)
        self.province = TurkishStr.upper(self.province)

    def add_report(self, report: ExamReport) -> ExamReport:
        try:
            self.get_report(report.descriptor.exam_name)
        except ValueError:
            self.reports.append(report)
            return report
        else:
            # return report
            raise ValueError(f"A report with name '{report.descriptor.exam_name}' already exists")

    def get_report(self, exam_name: str, soft_return: bool = False) -> ExamReport | None:
        for report in self.reports:
            if exam_name == report.descriptor.exam_name:
                return report
        if soft_return:
            return None
        raise ValueError(f"No report with name {exam_name}")
