# coding: utf-8


class _Error(Exception):

    def __init__(self, message, params=None):
        super(_Error, self).__init__(message, params)
        self.message = message
        self.params = params

    def __repr__(self):
        return self.message

    def __str__(self):
        return repr(self.message)


class ElementFoundError(_Error):
    pass


class TimeoutError(_Error):
    pass


class UDIDError(_Error):
    pass


class CommandError(_Error):
    pass


class ConfigError(_Error):
    pass


class ValidationError(_Error):
    pass


class RequestError(_Error):
    pass


class FormatError(_Error):
    pass


class UnknownError(_Error):
    pass


class IllegalError(_Error):
    pass
