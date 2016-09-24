from testix import suite
from startertests.asserts import *
from startertests import startertestcollection

class StarterTestSuite( startertestcollection.StarterTestCollection ):
	def starter_test_SuiteRunsOneTest( self ):
		class MySuite( suite.Suite ):
			def __init__( self ):
				self.wasRun = False
				suite.Suite.__init__( self )

			def test_FlagUp( self ):
				self.wasRun = True

		mySuite = MySuite()
		mySuite.run()
		STS_ASSERT( mySuite.wasRun )

	def starter_test_SuiteRunsMultipleTests( self ):
		class MultipleTestsSuite( suite.Suite ):
			def __init__( self ):
				self.wasRun = []
				suite.Suite.__init__( self )

			def test_First( self ):
				self.wasRun.append( 'First' )

			def test_Second( self ):
				self.wasRun.append( 'Second' )

			def test_Third( self ):
				self.wasRun.append( 'Third' )

		multipleTestSuite = MultipleTestsSuite()
		multipleTestSuite.run()
		STS_ASSERT_EQUALS( set( multipleTestSuite.wasRun ), set( [ 'First', 'Second', 'Third' ] ) )

	def starter_test_DontRunNonTestMethods( self ):
		class DontRunNonTestMethods( suite.Suite ):
			def __init__( self ):
				self.wasRun = False

			def notest_ThisShouldNotRun( self ):
				self.wasRun = True

		tested = DontRunNonTestMethods()
		tested.run()
		STS_ASSERT_EQUALS( tested.wasRun, False )

	def starter_test_SuiteClearsAllFakeObjectsBetweenTests( self ):
		class SomeSuite( suite.Suite ):
			def test_One( self ):
				self.fake1 = fakeobject.FakeObject( "fake" )

			def test_Two( self ):
				STS_ASSERT( self.fake1 is not fakeobject.FakeObject( "fake" ) )

		tested = SomeSuite()
		tested.run()

	def starter_test_Setup_and_Teardown( self ):
		class SetupAndTeardown( suite.Suite ):
			def test_X( self ):
				pass

			def setup( self ):
				self.calls.append( 'setup' )

			def teardown( self ):
				self.calls.append( 'teardown' )

		tested = SetupAndTeardown()
		tested.calls = []
		tested.run()
		tested.run()
		STS_ASSERT_EQUALS( tested.calls, [ 'setup', 'teardown', 'setup', 'teardown' ] )

StarterTestSuite()