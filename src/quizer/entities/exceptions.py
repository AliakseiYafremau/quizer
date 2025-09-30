class DomainError(Exception):
    pass


class AccessDeniedError(DomainError):
    pass


class DuplicateNameError(DomainError):
    pass
