import dataclasses

from examy.models.ExamReport import ExamReport


@dataclasses.dataclass
class Student:
    """Store student credentials to log in the result website and exam results of a student."""
    name: str
    """Name of student.
    
    Naturally identifies students but it may not be used as a primary key among students.
    It is also used to log in if `login_name` argument is not given.
    """
    number: int
    """School number of student.
    
    It is used for log in.
    """
    school: str
    """School name of student.
    
    It is used for log in.
    """
    province: str
    """Province of student's school.
    
    It is used for log in.
    """
    district: str
    """District of student's school.    
    
    It is used for log in.
    """
    grade_: dataclasses.InitVar[str | int]
    """Grade of student as an InitVar.
    
    A string is preferred for directly defining the grade option in login page.
    However, an integer is also accepted and will be converted to a string by adding ".Sınıf" suffix.
    """
    class_: str
    """Class identifier of student."""
    reports: list[ExamReport] = dataclasses.field(default_factory=list)
    """List of student's exam reports
    
    When initializing the student, it can be populated with previous ExamReport objects.
    
    After the initialization, use of `get_report()` and `add_report()` methods should be preferred instead of this attribute.
    """
    login_name: str = ""
    """Name used to log in for student.
    
    It is used to override the default login name, which is the first name of student's name.
    It can be useful for students with long first names.
    """
    grade: str = dataclasses.field(init=False)
    """Grade of student."""

    def __post_init__(self, grade_):
        # Set proper grade string from the given integer
        if isinstance(grade_, int):
            self.grade = str(grade_) + ".Sınıf"
        else:
            self.grade = grade_

        # Log in with the first name by default
        if not self.login_name:
            self.login_name = self.name.split()[0]

        # Fix capitalization
        from examy.utils import TurkishStr

        self.school = TurkishStr.upper(self.school)
        self.district = TurkishStr.upper(self.district)
        self.province = TurkishStr.upper(self.province)

    def add_report(self, report: ExamReport) -> ExamReport:
        """Add an exam report to student's reports list.

        It is checked that whether given report is already exist in the reports list.

        Args:
            report: Exam report to add.

        Returns:
            Added exam report. Same as `report` argument.

        Raises:
            ValueError: If given report already exists.
        """

        try:
            self.get_report(report.descriptor.exam_name)
        except ValueError:
            self.reports.append(report)
            return report
        else:
            # return report
            raise ValueError(f"A report with name '{report.descriptor.exam_name}' already exists")

    def get_report(self, exam_name: str, soft_return: bool = False) -> ExamReport | None:
        """Get an exam report from the results list by exam name.

        Args:
            exam_name: Name of the exam to search for.
            soft_return: If True return None if no report exists, instead of raising an exception.

        Returns:
            The exam report that matches the given exam name.
            None can also be returned, see `soft_return` argument.

        Raises:
            ValueError: If given report does not exist. Only if `soft_return` is False.
        """

        for report in self.reports:
            if exam_name == report.descriptor.exam_name:
                return report
        if soft_return:
            return None
        raise ValueError(f"No report with name {exam_name}")
