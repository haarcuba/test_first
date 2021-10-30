import pytest
from test_first.frequentlyused import *
from test_first import patch_module
from examples import calculator

class Test_Calculator:
    def construct( self, value ):
        self.tested = calculator.Calculator( value )

    @pytest.fixture
    def module_patch(self, patch_module):
        patch_module(calculator, 'multiplier')

    def test_Addition( self ):
        self.construct( 5 )
        self.tested.add( 7 )
        assert self.tested.result() == 12
        self.tested.add( 1.5 )
        assert self.tested.result() == 13.5

    def test_MultiplicationUsesMultiplier( self, module_patch ):
        self.construct( 5 )
        with Scenario() as s:
            s.multiplier.multiply( first = 5, second = 7 ) >> 35
            s.multiplier.multiply( first = 35, second = 10 ) >> 350
            self.tested.multiply( 7 )
            assert self.tested.result() == 35
            self.tested.multiply( 10 )
            assert self.tested.result() == 350
