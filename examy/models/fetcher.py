from abc import ABC, abstractmethod
from functools import wraps

from selenium.webdriver.remote.webdriver import WebDriver

from examy.models.ExamDescriptor import ExamDescriptor
from examy.models.ExamReport import ExamReport
from examy.models.Student import Student
from examy.models.exceptions import InvalidAction


class ExamFetcher(ABC):
    """Base class for fetchers"""

    result_page_layout: str
    fetcher_codename: str

    @staticmethod
    def check_fetch_arguments(func):
        @wraps(func)
        def wrapper(self: "ExamFetcher", student: Student, exam_descriptor: ExamDescriptor, *args, **kwargs):
            if exam_descriptor.result_page_layout != self.result_page_layout:
                raise ValueError(
                    f"Expected result page layout '{self.result_page_layout}', "
                    f"got '{exam_descriptor.result_page_layout}' instead."
                )
            return func(self, student, exam_descriptor, *args, **kwargs)

        return wrapper

    @check_fetch_arguments
    @abstractmethod
    def fetch(self, student: Student, exam_descriptor: ExamDescriptor, *args, **kwargs) -> ExamReport:
        pass


class SeleniumCompatibleFetcher(ExamFetcher, ABC):
    _driver: WebDriver

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, driver: WebDriver) -> None:
        self._driver = driver

    def is_driver_available(self) -> bool:
        return self._driver is not None

    @staticmethod
    def requires_driver(func):
        @wraps(func)
        def wrapper(self: "SeleniumCompatibleFetcher", *args, **kwargs):
            if not self.is_driver_available():
                raise InvalidAction(
                    "Attempted to execute an action with selenium without configuring any driver for " "the process"
                )
            return func(self, *args, **kwargs)

        return wrapper

    @requires_driver
    @ExamFetcher.check_fetch_arguments
    @abstractmethod
    def fetch(self, student, exam_descriptor, *args, **kwargs):
        pass
