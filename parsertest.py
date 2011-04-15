from simpleparse.common import numbers
from simpleparse.parser import Parser

import rollparse

parser = Parser(rollparse.declaration)

tests_success = [
    "d6",
    "5d6",
    "5d6 + d8",
    "(5d6 + d8)",
    "6 + (5d6 + d8)",
    "[5d6 + d8] + 6",
    "{3d20} + 10"
    ]

prod = "roll"

for test in tests_success:
    success, children, nextcharacter = parser.parse(test, production=prod)
    assert success and nextcharacter==len(test), """Wasn't able to parse %s as a %s (%s chars parsed of %s), returned value was %s"""%( repr(test), prod, nextcharacter, len(test), (success, children, nextcharacter))

tests_fail = [
    "{5d6}+{8d8}",
    "5d",
    "3+",
    "8d8" #this one should actually work
    ]

for test in tests_fail:
    success, children, nextcharacter = parser.parse(test, production=prod)
    if not (success and nextcharacter==len(test)):
        print """Wasn't able to parse %s as a %s (%s chars parsed of %s), returned value was %s\n"""%( repr(test), prod, nextcharacter, len(test), (success, children, nextcharacter))
