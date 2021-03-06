import uuid
from test_first import fake
from test_first import fake_privacy_violator
from . import base
from . import trivial
import test_first.expectations.call
from test_first import expectations

class Awaitable(base.Base):
    def __init__(self, call):
        self.__result = None
        id = str(uuid.uuid4())[-12:]
        self.__await_mock = fake.Fake(f'await on {call}@{id}')
        self.__exception_factory = None

    async def __call__(self):
        self.__await_mock()
        if self.__exception_factory is not None:
            raise self.__exception_factory()
        return self.__result

    def result(self):
        coroutine = self()
        return coroutine

    def set_result(self, result):
        self.__result = result

    def throwing(self, exception_factory):
        self.__exception_factory = exception_factory

    @property
    def further_expectation(self):
        path = fake_privacy_violator.path(self.__await_mock)
        return expectations.call.Call(path, trivial.Trivial)
