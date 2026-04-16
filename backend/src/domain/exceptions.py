class DomainException(Exception):
    message = "Unexpected error"


class FileMissingError(DomainException):
    def __init__(self, file_id=None):
        self.message = f"File not found"
        self.file_id = file_id


class FileEmptyError(DomainException):
    def __init__(self, file_id=None):
        self.message = f"File is empty"
        self.file_id = file_id
