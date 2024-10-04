class FetcherFailure(Exception):
    """A problem in the fetching operation."""
    pass


class InvalidAction(Exception):
    """An invalid action was requested."""
    pass


class StudentDidNotTakeExam(FetcherFailure):
    """A student did not take the exam."""
    pass


class StudentNotFound(FetcherFailure):
    """Student was not found in the result website.

    This **might** mean that student did not take the exam."""
    pass
