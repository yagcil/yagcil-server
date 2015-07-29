"""
    All error handlers used by the API Server
"""
from enum import IntEnum


class ErrorCode(IntEnum):
    """API Server error codes"""
    UndefinedError = -1
    # ResourceNotFound
    TaskNotFound = 10


class AbstractError(Exception):
    """An abstract API error class"""

    def __init__(self, message, error_code=ErrorCode.UndefinedError,
                 status_code=None, payload=None):
        """Initialize API error instance
        :param str message: Error message
        :param ErrorCode error_code: API server error code
        :param int status_code: HTTP status code
        :param payload: HTTP payload
        """
        Exception.__init__(self)
        self.message = message
        self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        """
        Serialize error data
        :return: A dictionary filled with serialized error's data
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error'] = {
            'name': "{0}: {1}".format(
                type(self).__name__,
                self.error_code.name
            ),
            'code': self.error_code
        }

        return rv


class ResourceNotFound(AbstractError):
    status_code = 404

