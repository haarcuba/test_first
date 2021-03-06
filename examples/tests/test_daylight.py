import pytest
from test_first.frequentlyused import *
from test_first import patch_module

from examples import daylight
class FakeDay( object ):
        def __add__( self, other ):
                return other

class Test_Daylight:
    @pytest.fixture
    def module_patch( self, patch_module ):
        patch_module( daylight, 'datetime' )

    def test_Main( self, module_patch ):
        with Scenario() as s:
            fakeDay = FakeDay()
            fakeDay.hour = 12
            s.datetime.date.today() >> fakeDay
            s.datetime.datetime.today() >> fakeDay
            s.datetime.timedelta(IgnoreArgument()) >> FakeDay()
            nextDay = daylight.nextDaylightDate()
            assert nextDay is not fakeDay

    def test_EarlyInTheMorningUsesSameDate( self, module_patch ):
        with Scenario() as s:
            fakeDay = FakeDay()
            fakeDay.hour = 2
            s.datetime.date.today() >> fakeDay
            s.datetime.datetime.today() >> fakeDay
            nextDay = daylight.nextDaylightDate()
            assert nextDay is fakeDay
