import hypothesis
import hypothesis.strategies as strategies
import pytest
from test_first import fake
from test_first import scenario
from test_first import test_first_exception
from test_first import argumentexpectations

class TestArgumentExpectations:
    @hypothesis.given(A=strategies.integers(),B=strategies.integers())
    def test_argument_equals_raises_when_called_with_wrong_arguments(self, A, B):
        hypothesis.assume( A != B )
        fakeObject = fake.Fake('some_object')
        with scenario.Scenario() as s:
            s.some_object( A ) >> 'first'
            s.some_object( B ) >> 'second'
            assert fakeObject( A ) == 'first'
            with pytest.raises( test_first_exception.ExpectationException ):
                fakeObject( A )

    def test_argument_is_fake_object_with_path( self ):
        fakeObject = fake.Fake('some_object')
        with scenario.Scenario() as s:
            s.some_object( argumentexpectations.ArgumentIsFakeObjectWithPath( 'another_fake_object' ) ) >> 'the result'
            s.some_object( argumentexpectations.ArgumentIsFakeObjectWithPath( 'yet_another' ) ) >> 'another result'
            assert fakeObject(fake.Fake('another_fake_object')) == 'the result'
            assert fakeObject(fake.Fake('yet_another')) == 'another result'

    def test_FakeObjectExpectation( self ):
        fakeObject = fake.Fake('some_object')
        fakeArgument = fake.Fake('fake_argument')
        with scenario.Scenario() as s:
            s.some_object(fake.Fake('fake_argument'))
            fakeObject( fakeArgument )

    def test_IgnoreArgument( self ):
        fakeObject = fake.Fake('some_object')
        with scenario.Scenario() as s:
            s.some_object( 10 ) >> 'first'
            s.some_object( argumentexpectations.IgnoreArgument() ) >> 'second'
            assert fakeObject( 10 ) == 'first'
            assert fakeObject( "this doens't matter" ) == 'second'

    def test_IgnoreCallDetails(self):
        fakeObject = fake.Fake('some_object')
        with scenario.Scenario() as s:
            s.some_object( 10 ) >> 'first'
            s.some_object( argumentexpectations.IgnoreCallDetails() ) >> 'second'
            s.another_object(argumentexpectations.IgnoreCallDetails())
            assert fakeObject( 10 ) == 'first'
            assert fakeObject( "this doens't matter", "this doens'nt either", this='does not matter also', that='neither' ) == 'second'
            with pytest.raises( test_first_exception.ExpectationException ):
                fakeObject("this is an unexpected call: verify that IgnoreCallDetails() still leaves the Fake object's path verification intact")

    def test_KeywordArguments( self ):
        fakeObject = fake.Fake('some_object')
        with scenario.Scenario() as s:
            s.some_object( 10, name = 'Lancelot' ).returns( 'first' )
            s.some_object( 11, name = 'Galahad' ).returns( 'second' )
            assert fakeObject( 10, name = 'Lancelot' ) == 'first'
            with pytest.raises( test_first_exception.ExpectationException ):
                fakeObject( 11, name = 'not Galahad'  )
