from typing import Iterator

from examy.models.ExamDescriptor import ExamDescriptor
from examy.models.ExamReport import ExamReport
from examy.models.Student import Student


class ResultExporter(object):
    export_dict_student = {
        "name": ["Student", "name"],
        "number": ["Student", "number"],
        "class": ["Student", "class_"],
        "class_rank": ["Ranking", "class_rank"],
        "school_rank": ["Ranking", "school_rank"],
        "district_rank": ["Ranking", "district_rank"],
        "province_rank": ["Ranking", "province_rank"],
        "global_rank": ["Ranking", "global_rank"],
        "score": ["Report", "score"],
        "true_count": ["Report", "true_count"],
        "false_count": ["Report", "false_count"],
        "empty_count": ["Report", "empty_count"],
        "net": ["Report", "net"],
        "group1": [
            "group",
            {
                "{short_test_name}_true": ["TestResult", "true_count"],
                "{short_test_name}_false": ["TestResult", "false_count"],
                "{short_test_name}_empty": ["TestResult", "empty_count"],
                "{short_test_name}_net": ["TestResult", "net"],
            },
        ],
    }

    export_dict_common = {
        "school_attendance": ["Ranking", "school_attendance"],
        "district_attendance": ["Ranking", "district_attendance"],
        "province_attendance": ["Ranking", "province_attendance"],
        "global_attendance": ["Ranking", "global_attendance"],
        "question_count": ["Report", "question_count"],
        "group1": [
            "group",
            {
                "{short_test_name}_question_count": ["Test", "question_count"],
            },
        ],
    }

    def __init__(self):
        self.student_export = []
        self.student_export_headers = []
        self.common_export = []
        self.common_export_headers = []

    def clear(self):
        self.student_export = []
        self.common_export = []

    @staticmethod
    def _make_export(st: Student, desc: ExamDescriptor, report: ExamReport, export_scheme: dict) -> list:
        export = []

        for k, v in export_scheme.items():
            obj, attrib = v
            match obj:
                case "group":
                    for td, tr in report.iter_tests():
                        for k2, (obj2, attrib2) in attrib.items():
                            if obj2 == "Test":
                                export.append(td.__getattribute__(attrib2))
                            else:
                                export.append(tr.__getattribute__(attrib2))
                case "Student":
                    export.append(st.__getattribute__(attrib))
                case "Report":
                    export.append(report.__getattribute__(attrib))
                case "Ranking":
                    export.append(report.ranks.__getattribute__(attrib))
        return export

    @staticmethod
    def _make_headers(st: Student, desc: ExamDescriptor, report: ExamReport, export_scheme: dict) -> list:
        headers = []
        for k, v in export_scheme.items():
            obj, attrib = v
            match obj:
                case "group":
                    for td, tr in report.iter_tests():
                        for k2, _ in attrib.items():
                            headers.append(k2.format(short_test_name=td.short_name))
                case _:
                    headers.append(k)
        return headers

    def create_export_from_students(self, st_gen: Iterator[Student], desc: ExamDescriptor):
        commons_set = False
        for st in st_gen:
            report = st.get_report(desc.exam_name, soft_return=True)
            if report is None:
                continue
            self.student_export.append(self._make_export(st, desc, report, self.export_dict_student))
            if not commons_set:
                commons_set = True
                self.student_export_headers = self._make_headers(st, desc, report, self.export_dict_student)

                self.common_export_headers = self._make_headers(st, desc, report, self.export_dict_common)
                self.common_export = self._make_export(st, desc, report, self.export_dict_common)

    def sort(self, by: str, reverse: bool = False):
        index = self.student_export_headers.index(by)
        self.student_export.sort(key=lambda x: x[index], reverse=reverse)

    def to_csv(self, student_path: str, common_path: str):
        import csv

        with open(student_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.student_export_headers)
            writer.writerows(self.student_export)
        with open(common_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.common_export_headers)
            writer.writerow(self.common_export)
