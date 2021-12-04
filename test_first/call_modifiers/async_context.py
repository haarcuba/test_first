from test_first import fake
from test_first import fake_privacy_violator
import test_first.expectations.call
from test_first import expectations
import uuid
from . import base
from . import trivial

class AsyncContext(base.Base):
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__aenter_mock = fake.Fake(f'{call}@{id}.__aenter__')

    async def __aenter__(self):
        self.__aenter_mock()
        return self.__result

    async def __aexit__(self, exception_type, exception_value, traceback):
        pass

    @property
    def further_expectation(self):
        path = fake_privacy_violator.path(self.__aenter_mock)
        return expectations.call.Call(path, trivial.Trivial)

    def set_result(self, value):
        self.__result = value

    def throwing(self, exception_factory):
        pass

    def result(self):
        return self

    def __repr__(self):
        return f'AsyncContext({self.__result})'
