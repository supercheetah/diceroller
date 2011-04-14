import unittest
import mx_test, test_objectgenerator, test_simpleparsegrammar
import test_common_chartypes, test_common_numbers, test_common_iso_date
import test_common_strings, test_printers
import test_xml

import string
from mx import TextTools
mxVersion = tuple(string.split( TextTools.__version__, '.'))
print "mxVersion:", mxVersion
mxVersion = mxVersion[:3]

def getSuite():
	set = []
	for module in [
		mx_test,
		test_objectgenerator,
		test_simpleparsegrammar,
		test_common_chartypes,
		test_common_numbers,
		test_common_iso_date,
		test_common_strings,
		test_printers,
		test_xml,
	]:
		set.append( module.getSuite() )
##	set = set * 20
	return unittest.TestSuite(
		set
	)

if __name__ == "__main__":
	unittest.main(defaultTest="getSuite")
