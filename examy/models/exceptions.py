class FetcherFailure(Exception):
    pass


class InvalidAction(Exception):
    pass


class StudentDidNotTakeExam(FetcherFailure):
    pass


class StudentNotFound(FetcherFailure):
    pass
