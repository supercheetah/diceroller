from simpleparse import generator
from simpleparse.objectgenerator import *
GENERATOR = generator.Generator ()

class Parser:
	'''Mix-in class for simpleparse.parser.Parser which uses this GENERATOR
	to build tagging tables.  You'll likely want to override __init__ to avoid
	building a new parser from a grammar (or subclass BaseParser instead of
	Parser)
	'''
	def buildTagger( self, name=None, processor = None ):
		'''Build the tag-table for parsing the EBNF for this parser'''
		return GENERATOR.buildParser( name, processor )

GENERATOR.addDefinition(
    'declarationset',
    Name(
        report = 1,
        lookahead = 0,
        repeating = 1,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = 'declaration',
    ),
)
GENERATOR.addDefinition(
    'declaration',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            FirstOfGroup(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'unreportedname',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'expandedname',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'name',
                    ),
                ],
                negative = 0,
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = ':',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = ':',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '=',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'seq_group',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'element_token',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'lookahead_indicator',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'negpos_indicator',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            FirstOfGroup(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'literal',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'range',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'group',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'name',
                    ),
                ],
                negative = 0,
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'occurence_indicator',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'error_on_fail',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'negpos_indicator',
    Range(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = '-+',
    ),
)
GENERATOR.addDefinition(
    'lookahead_indicator',
    Literal(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = '?',
    ),
)
GENERATOR.addDefinition(
    'occurence_indicator',
    Range(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = '+*?',
    ),
)
GENERATOR.addDefinition(
    'error_on_fail',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '!',
            ),
            SequentialGroup(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'ts',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'literal',
                    ),
                ],
                negative = 0,
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'group',
    SequentialGroup(
        report = 1,
        expanded = 1,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '(',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'seq_group',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = ')',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'seq_group',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
            FirstOfGroup(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'error_on_fail',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'fo_group',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'element_token',
                    ),
                ],
                negative = 0,
            ),
            SequentialGroup(
                lookahead = 0,
                repeating = 1,
                optional = 1,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'ts',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'seq_indicator',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'ts',
                    ),
                    FirstOfGroup(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        children = [
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'error_on_fail',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'fo_group',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'element_token',
                            ),
                        ],
                        negative = 0,
                    ),
                ],
                negative = 0,
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ts',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'fo_group',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'element_token',
            ),
            SequentialGroup(
                lookahead = 0,
                repeating = 1,
                optional = 0,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'ts',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'fo_indicator',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'ts',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'element_token',
                    ),
                ],
                negative = 0,
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'fo_indicator',
    Literal(
        report = 0,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = '/',
    ),
)
GENERATOR.addDefinition(
    'seq_indicator',
    Literal(
        report = 0,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = ',',
    ),
)
GENERATOR.addDefinition(
    'unreportedname',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '<',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'name',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '>',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'expandedname',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '>',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'name',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '<',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'name',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_',
            ),
            Range(
                lookahead = 0,
                repeating = 1,
                optional = 1,
                negative = 0,
                value = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'ts',
    FirstOfGroup(
        report = 0,
        lookahead = 0,
        repeating = 1,
        expanded = 0,
        optional = 1,
        children = [
            Range(
                lookahead = 0,
                repeating = 1,
                optional = 0,
                negative = 0,
                value = ' \t\n\x0b\x0c\r',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'comment',
            ),
        ],
        negative = 0,
    ),
)
GENERATOR.addDefinition(
    'comment',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '#',
            ),
            Literal(
                lookahead = 0,
                repeating = 1,
                optional = 0,
                negative = 1,
                value = '\n',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '\n',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'literal',
    FirstOfGroup(
        report = 1,
        expanded = 0,
        children = [
            SequentialGroup(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                children = [
                    Literal(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = "'",
                    ),
                    FirstOfGroup(
                        lookahead = 0,
                        repeating = 1,
                        optional = 1,
                        children = [
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'CHARNOSNGLQUOTE',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'ESCAPEDCHAR',
                            ),
                        ],
                        negative = 0,
                    ),
                    Literal(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = "'",
                    ),
                ],
                negative = 0,
            ),
            SequentialGroup(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                children = [
                    Literal(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = '"',
                    ),
                    FirstOfGroup(
                        lookahead = 0,
                        repeating = 1,
                        optional = 1,
                        children = [
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'CHARNODBLQUOTE',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'ESCAPEDCHAR',
                            ),
                        ],
                        negative = 0,
                    ),
                    Literal(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = '"',
                    ),
                ],
                negative = 0,
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'range',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '[',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'CHARBRACE',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'CHARDASH',
            ),
            FirstOfGroup(
                lookahead = 0,
                repeating = 1,
                optional = 1,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'CHARRANGE',
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'CHARNOBRACE',
                    ),
                ],
                negative = 0,
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = 'CHARDASH',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = ']',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'CHARBRACE',
    Literal(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = ']',
    ),
)
GENERATOR.addDefinition(
    'CHARDASH',
    Literal(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = '-',
    ),
)
GENERATOR.addDefinition(
    'CHARRANGE',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'CHARNOBRACE',
            ),
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '-',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'CHARNOBRACE',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'CHARNOBRACE',
    FirstOfGroup(
        report = 1,
        expanded = 0,
        children = [
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'ESCAPEDCHAR',
            ),
            Name(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = 'CHAR',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'CHAR',
    Range(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 1,
        value = ']',
    ),
)
GENERATOR.addDefinition(
    'ESCAPEDCHAR',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Literal(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '\\',
            ),
            FirstOfGroup(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                children = [
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'SPECIALESCAPEDCHAR',
                    ),
                    SequentialGroup(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        children = [
                            Literal(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'x',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'HEXESCAPEDCHAR',
                            ),
                        ],
                        negative = 0,
                    ),
                    SequentialGroup(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        children = [
                            Literal(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'u',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'UNICODEESCAPEDCHAR_16',
                            ),
                        ],
                        negative = 0,
                    ),
                    SequentialGroup(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        children = [
                            Literal(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'U',
                            ),
                            Name(
                                lookahead = 0,
                                repeating = 0,
                                optional = 0,
                                negative = 0,
                                value = 'UNICODEESCAPEDCHAR_32',
                            ),
                        ],
                        negative = 0,
                    ),
                    Name(
                        lookahead = 0,
                        repeating = 0,
                        optional = 0,
                        negative = 0,
                        value = 'OCTALESCAPEDCHAR',
                    ),
                ],
                negative = 0,
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'SPECIALESCAPEDCHAR',
    Range(
        report = 1,
        lookahead = 0,
        repeating = 0,
        expanded = 0,
        optional = 0,
        negative = 0,
        value = '\\abfnrtv"\'',
    ),
)
GENERATOR.addDefinition(
    'OCTALESCAPEDCHAR',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '01234567',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = '01234567',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 1,
                negative = 0,
                value = '01234567',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'HEXESCAPEDCHAR',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'CHARNODBLQUOTE',
    Range(
        report = 1,
        lookahead = 0,
        repeating = 1,
        expanded = 0,
        optional = 0,
        negative = 1,
        value = '\\"',
    ),
)
GENERATOR.addDefinition(
    'CHARNOSNGLQUOTE',
    Range(
        report = 1,
        lookahead = 0,
        repeating = 1,
        expanded = 0,
        optional = 0,
        negative = 1,
        value = "\\'",
    ),
)
GENERATOR.addDefinition(
    'UNICODEESCAPEDCHAR_16',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
        ],
    ),
)
GENERATOR.addDefinition(
    'UNICODEESCAPEDCHAR_32',
    SequentialGroup(
        report = 1,
        expanded = 0,
        children = [
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
            Range(
                lookahead = 0,
                repeating = 0,
                optional = 0,
                negative = 0,
                value = '0123456789abcdefABCDEF',
            ),
        ],
    ),
)
