from typing import Any

from examy.models.Student import Student


class StudentGroup:
    def __init__(self, common_attribs: dict[str, Any], friendly_name: str = None):
        self.common_attribs = common_attribs
        self._friendly_name = friendly_name
        self._students: list[Student] = []

    @property
    def friendly_name(self) -> str:
        return self._friendly_name

    @friendly_name.setter
    def friendly_name(self, value: str):
        self._friendly_name = value

    def __len__(self) -> int:
        return len(self._students)

    def __str__(self):
        return f'StudentGroup "{self.friendly_name}" with {len(self)} students, common_attribs={self.common_attribs}"'

    def add_student(self, unique_attribs: dict[str, Any]) -> Student:
        new = Student(**self.common_attribs, **unique_attribs)
        self._students.append(new)
        return new

    def add_students(self, unique_attribs_list: list[dict[str, Any]]):
        for unique_attribs in unique_attribs_list:
            self.add_student(unique_attribs)

    def iter_students(self):
        for student in self._students:
            yield student
