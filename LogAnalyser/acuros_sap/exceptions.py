import inspect
class ASAPError(Exception):
    def __init__ (self, message):
        self.caller = inspect.stack()[2]
        self.message = message

    def __str__ (self):
        return self.message
    


class UnsupportedRequestMethodError(ASAPError):
    pass

class UnsupportedVersionError(ASAPError):
    pass

class NoParameterError(ASAPError):
    pass

class InvalidParameterError(ASAPError):
    pass

class WrongFormatError(ASAPError):
    pass

class NotAuthenticatedUserError(ASAPError):
    pass

class InternalServerError(ASAPError):
    pass

class IllegalStateError(ASAPError):
    pass

class TimeExpiredError(ASAPError):
    pass
