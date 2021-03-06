from test_first import fake
from test_first import fake_privacy_violator
import test_first.expectations.call
from test_first import expectations
from . import trivial
import uuid
from . import base

class SyncContext(base.Base):
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__enter_mock = fake.Fake(f'{call}@{id}.__enter__')

    def __enter__(self):
        self.__enter_mock()
        return self.__result

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    @property
    def further_expectation(self):
        path = fake_privacy_violator.path(self.__enter_mock)
        return expectations.call.Call(path, trivial.Trivial)

    def set_result(self, value):
        self.__result = value

    def throwing(self, exception_factory):
        pass

    def result(self):
        return self

    def __repr__(self):
        return f'SyncContext({self.__result})'
