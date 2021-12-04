from . import call_character
from test_first import test_first_exception
import test_first.expectations.call
from test_first import expectations
import test_first.call_modifiers.sync_context
import test_first.call_modifiers.async_context
import test_first.call_modifiers.awaitable
import test_first.call_modifiers.trivial
from test_first import call_modifiers

class ExpectationMaker:
    def __init__(self, scenario, scenarioMocks, path, character: call_character.CallCharacter):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__character = character

    def __getattr__( self, name ):
        child_path = f'{self.__path}.{name}'
        return ExpectationMaker(self.__scenario, self.__scenarioMocks, child_path, self.__character)

    def __call__(self, *args, **kwargs):
        call = self.__generate_expectation(*args, **kwargs)
        self.__scenario.addEvent(call)
        if call.further_expectation is not None:
            self.__scenario.addEvent(call.further_expectation)
        return call

    def __generate_expectation(self, *args, **kwargs):
        if self.__character.normal:
            modifier = call_modifiers.trivial.Trivial
        if self.__character.awaitable:
            modifier = call_modifiers.awaitable.Awaitable
        if self.__character.is_sync_context:
            modifier = call_modifiers.sync_context.SyncContext
        if self.__character.is_async_context:
            modifier = call_modifiers.async_context.AsyncContext

        return expectations.call.Call(self.__path, modifier, *args, **kwargs)
