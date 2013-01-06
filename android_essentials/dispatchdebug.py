import rollparse
import logging

logging.basicConfig(level=logging.DEBUG)

production = "roll"

rollparser = rollparse.RollParser( rollparse.declaration )

rollparse.solve_roll("2x2d8*2+3")

rollparse.solve_roll("d8")

rollparser.parse("[d6+d8+5]+3", processor=rollparse.lexer.Lexer() )

rollparser.parse("{2xd6}+3+3xd8", processor=rollparse.lexer.Lexer() )

rollparser.parse("{2xd6]+3+3xd8", processor=rollparse.lexer.Lexer() ) #should give error
