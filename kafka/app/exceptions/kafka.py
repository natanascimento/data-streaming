from app.exceptions.base import BaseException


class ConsumerError(BaseException):

    def __init__(self, msg):
        super().__init__(msg)