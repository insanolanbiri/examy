import logging
import threading
from typing import Callable, Sequence

from selenium.webdriver.remote.webdriver import WebDriver

from examy.models.ExamDescriptor import ExamDescriptor
from examy.models.Student import Student
from examy.models.exceptions import StudentDidNotTakeExam
from examy.models.fetcher import ExamFetcher, SeleniumCompatibleFetcher
from examy.utils.stgroup import StudentGroup

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, webdriver_generator: Callable[[], WebDriver] | None = None):
        self.errored_students: dict[str, list[Student]] = {}
        self.errored_students_lock = threading.Lock()
        self._groups: list[StudentGroup] = []
        self.webdriver_generator = webdriver_generator

        self._drivers: dict = {}
        self._exam_descriptor: ExamDescriptor | None = None
        self._fetcher_type: type[ExamFetcher] | None = None

    @property
    def groups(self) -> list[StudentGroup]:
        return self._groups

    @groups.setter
    def groups(self, groups: list[StudentGroup]) -> None:
        self._groups = groups

    def add_group(self, group: StudentGroup) -> None:
        self._groups.append(group)

    def add_groups(self, groups: Sequence[StudentGroup]):
        self._groups.extend(groups)

    @property
    def total_student_count(self) -> int:
        return sum((len(g) for g in self.groups))

    def __str__(self):
        return f"Manager with {len(self._groups)} groups containing {self.total_student_count} students in total"

    def students(self):
        for group in self._groups:
            for st in group.iter_students():
                yield st

    def _set_driver(self) -> None:
        if issubclass(self._fetcher_type, SeleniumCompatibleFetcher):
            self._drivers[threading.current_thread().name] = self.webdriver_generator()

    def _fetch_single(self, st: Student):
        fetcher = self._fetcher_type()
        if isinstance(fetcher, SeleniumCompatibleFetcher):
            fetcher.driver = self._drivers[threading.current_thread().name]

        err_list = self.errored_students[self._exam_descriptor.exam_name]

        try:
            fetcher.fetch(st, self._exam_descriptor)
            res = st.reports[-1]
            logger.info(
                f"{st.name}: ok; score={res.score}, net={res.net}, "
                f"class_rank={res.ranks.class_rank}, school_rank={res.ranks.school_rank}"
            )
            with self.errored_students_lock:
                if st in err_list:
                    err_list.remove(st)
        except StudentDidNotTakeExam:
            logger.info(f"{st.name} did not take the exam named '{self._exam_descriptor.exam_name}'")
        except:
            with self.errored_students_lock:
                if st not in err_list:
                    err_list.append(st)
            logger.error(f"Failed to fetch results of {st.name}", exc_info=True)

    def fetch_multithread(
        self,
        exam_descriptor: ExamDescriptor,
        fetcher_type: type[ExamFetcher],
        subset: str = "all",
        max_workers: int | None = None,
    ):
        from concurrent.futures.thread import ThreadPoolExecutor

        self._fetcher_type = fetcher_type
        self._exam_descriptor = exam_descriptor
        err_list = self.errored_students.get(exam_descriptor.exam_name, list())
        self.errored_students[exam_descriptor.exam_name] = err_list

        if subset == "all":
            students_to_fetch = self.students()
            count = self.total_student_count
        elif subset == "errored":
            students_to_fetch = err_list[:]
            count = len(students_to_fetch)
        else:
            raise ValueError(f"Invalid subset '{subset}'")

        with ThreadPoolExecutor(initializer=self._set_driver, max_workers=max_workers) as executor:
            for i, _ in enumerate(executor.map(self._fetch_single, students_to_fetch), 1):
                # for loop is required for waiting for the results
                logger.debug(f"{i}/{count} done.")

        for i in self._drivers.values():
            i.quit()

        self._drivers = {}
        self._fetcher_type = None
        self._exam_descriptor = None
