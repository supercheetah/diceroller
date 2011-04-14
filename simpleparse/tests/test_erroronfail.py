import unittest, pprint
from simpleparse.parser import Parser
from simpleparse.error import ParserSyntaxError

class ErrorOnFailTests( unittest.TestCase ):
	"""Tests of the error-on failure mechanisms"""
	def shouldRaise(self, definition, parserName, testValue, ):
		self.failUnlessRaises( ParserSyntaxError,  Parser( definition).parse, testValue, parserName )
	def shouldNotRaise(self, definition, parserName, testValue, ):
		success,result, next = Parser( definition).parse( testValue, parserName )
		assert success, """Didn't parse %s (error on fail test for definition %s)"""%( repr(testValue), repr(definition))
		

	def testErrorOnFail1( self ):
		self.shouldRaise(
			'''s := -trailer!
			trailer   := "bad"
			''',
			's',
			'badba',
		)
	def testErrorOnFail2( self ):
		self.shouldRaise(
			'''s := -"bad"!
			''',
			's',
			'badba',
		)
	def testErrorOnFail3( self ):
		self.shouldRaise(
			'''s := -(a,b)!
			a := "a"
			b := "b"
			''',
			's',
			'abdba',
		)
	def testErrorOnFail4( self ):
		self.shouldRaise(
			'''s := -[ab]!
			''',
			's',
			'abdba',
		)
	
	def testErrorOnFail5( self ):
		self.shouldRaise(
			'''s := !,'a','b'
			''',
			's',
			'badba',
		)
	def testErrorOnFail6( self ):
		self.shouldNotRaise(
			'''s := 'a',!,'b'
			''',
			's',
			'abdba',
		)
	def testErrorOnFail7( self ):
		self.shouldNotRaise(
			'''s := 'a',!,'b'?
			''',
			's',
			'acbdba',
		)
	def testErrorOnFail8( self ):
		self.shouldRaise(
			'''s := 'a',!,'b'
			''',
			's',
			'acbdba',
		)

def getSuite():
	return unittest.makeSuite(ErrorOnFailTests,'test')

if __name__ == "__main__":
	unittest.main(defaultTest="getSuite")
