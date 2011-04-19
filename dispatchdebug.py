import rollparse
import logging

logging.basicConfig(level=logging.DEBUG)

production = "roll"

rollparser = rollparse.RollParser( rollparse.declaration )

rollparser.parse("[d6+d8+5]+3", processor=rollparse.lexer.Lexer() )

rollparser.parse("{2xd6}+3+3xd8", processor=rollparse.lexer.Lexer() )

rollparser.parse("{2xd6]+3+3xd8", processor=rollparse.lexer.Lexer() ) #should give error
