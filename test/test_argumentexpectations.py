import hypothesis
import hypothesis.strategies as strategies
import pytest
from testix import fakeobject
from testix import scenario
from testix import testixexception
from testix import argumentexpectations

class TestArgumentExpectations:
    @hypothesis.given(A=strategies.integers(),B=strategies.integers())
    def test_argument_equals_raises_when_called_with_wrong_arguments(self, A, B):
        hypothesis.assume( A != B )
        fakeObject = fakeobject.FakeObject( 'some_object' )
        with scenario.Scenario() as s:
            s.some_object( A ) >> 'first'
            s.some_object( B ) >> 'second'
            assert fakeObject( A ) == 'first'
            with pytest.raises( testixexception.ExpectationException ):
                fakeObject( A )

    def test_argument_is_fake_object_with_path( self ):
        fakeObject = fakeobject.FakeObject( 'some_object' )
        with scenario.Scenario() as s:
            s.some_object( argumentexpectations.ArgumentIsFakeObjectWithPath( 'another_fake_object' ) ) >> 'the result'
            s.some_object( argumentexpectations.ArgumentIsFakeObjectWithPath( 'yet_another' ) ) >> 'another result'
            assert fakeObject( fakeobject.FakeObject( 'another_fake_object' ) ) == 'the result'
            assert fakeObject( fakeobject.FakeObject( 'yet_another' ) ) == 'another result'

    def test_FakeObjectExpectation( self ):
        fakeObject = fakeobject.FakeObject( 'some_object' )
        fakeArgument = fakeobject.FakeObject( 'fake_argument' )
        with scenario.Scenario() as s:
            s.some_object( fakeobject.FakeObject( 'fake_argument' ) )
            fakeObject( fakeArgument )

    def test_IgnoreArgument( self ):
        fakeObject = fakeobject.FakeObject( 'some_object' )
        with scenario.Scenario() as s:
            s.some_object( 10 ) >> 'first'
            s.some_object( argumentexpectations.IgnoreArgument() ) >> 'second'
            assert fakeObject( 10 ) == 'first'
            assert fakeObject( "this doens't matter" ) == 'second'

    def test_KeywordArguments( self ):
        fakeObject = fakeobject.FakeObject( 'some_object' )
        with scenario.Scenario() as s:
            s.some_object( 10, name = 'Lancelot' ).returns( 'first' )
            s.some_object( 11, name = 'Galahad' ).returns( 'second' )
            assert fakeObject( 10, name = 'Lancelot' ) == 'first'
            with pytest.raises( testixexception.ExpectationException ):
                fakeObject( 11, name = 'not Galahad'  )