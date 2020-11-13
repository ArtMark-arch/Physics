class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


class AuthorizationError(Exception):
    pass


class AbsenceError(AuthorizationError):
    pass


class FreeLoginError(AuthorizationError):
    pass


class BadDataError(AuthorizationError):
    pass


class GraphicError(Exception):
    pass


class EmptyValueError(GraphicError):
    pass


class AvailableValueError(GraphicError):
    pass


class BadTimeError(GraphicError):
    pass


class NotPickError(GraphicError):
    pass
