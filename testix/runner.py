from testix import suite
import subprocess
import sys
import os

class Runner( object ):
	def __init__( self, pythonFiles ):
		self._pythonFiles = pythonFiles
		self._total = 0
		self._work()
		print '%d test(s) were run' % self._total
		print 'OK!'

	def _work( self ):
		for path in self._pythonFiles:
			directory, sourceFile = os.path.dirname( path ), os.path.basename( path )
			moduleName = sourceFile.split( '.' )[ 0 ]
			self._runModule( directory, moduleName )

	def _runModule( self, directory, moduleName ):
			CODE_TEMPLATE = \
					'from testix import suite; import %(module)s as module\n' \
					'testSuiteCandidates = [ getattr( module, name ) for name in dir( module ) if name.startswith( "Test" ) ]\n' \
					"suiteClass = [ s for s in testSuiteCandidates if issubclass( s, suite.Suite ) ][ 0 ]\n" \
					"suiteObject = suiteClass()\n" \
					"suiteObject.run()\n" \
					'print "\\n%%s" %% suiteObject.totalTestsRun()'
			code = CODE_TEMPLATE % dict( module = moduleName )
			print 'running test suite %s: ' % moduleName, 
			self._runPythonCode( directory, code )

	def _runPythonCode( self, directory, code ):
			process = subprocess.Popen( "python -c '%s'" % code, cwd = directory, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
			output, unused = process.communicate()
			if process.returncode != 0:
				print output
				quit( -1 )
			else:
				lines = output.split( '\n' )
				lastLine = lines[ -2 ]
				testsRun = int( lastLine.strip() )
				print '%d test(s)' % testsRun
				self._total += testsRun

if __name__ == '__main__':
	Runner( sys.argv[ 1: ] )
