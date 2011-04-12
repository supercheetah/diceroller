import parser
import logging

logging.basicConfig(level=logging.DEBUG)

production = "roll"

rollparser = parser.RollParser( parser.declaration )

rollparser.parse("[d6+d8+5]+3", processor=parser.dispatcher.RollDispatcher() )

rollparser.parse("{2xd6}+3+3xd8", processor=parser.dispatcher.RollDispatcher() )
