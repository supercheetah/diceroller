from mx import TextTools
from mx.TextTools import *
import pprint, string

class TagTableFormatter:
	def __init__(
		self,
		flagNames = (
			"CallTag",
			"AppendMatch",
			"AppendToTagobj",
			"AppendTagobj",
			"LookAhead",
		),
		commandNames = (
			"Fail",
			"Jump",
			"AllIn",
			"AllNotIn",
			"AllInSet",
			"AllInCharSet",
			"Is",
			"IsNot",
			"IsIn",
			"IsNotIn",
			"IsInSet",
			"IsInCharSet",
			"Word",
			"WordStart",
			"WordEnd",
			"sWordStart",
			"sWordEnd",
			"sFindWord",
			"Call",
			"CallArg",
			"Table",
			"SubTable",
			"TableInList",
			"SubTableInList",
			"EOF",
			"Skip",
			"Move",
			"JumpTarget",
			"Loop",
			"LoopControl",
		),
		specialNames = (
			"To",
			"Here",
			"MatchOk",
			"MatchFail",
			"ToBOF",
			"ToEOF",
			"ThisTable",
		),
	):
		for attribute, set in map(None, ["flags","commands","special"],[flagNames, commandNames, specialNames]):
			entries = []
			for name in flagNames:
				try:
					entries.append( (name, getattr(TextTools,name)))
				except AttributeError:
					pass
			setattr( self, attribute, entries)
			
	def item( self, entry ):
		"""Display an entry as a human-friendly piece of source-code"""
		tagobj, command, command_argument = entry[:3]
		if len(entry) > 3:
			jump_no_match = entry[3]
			if len(entry)>4:
				jump_match = entry[4]
		command = self.decomposeCommand( command )
		items = [ ]
		items.append( repr( tagobj) )
		items.append( string.join(command, '+'))
##		if command[0] in ('Table','SubTable'):
##			items.append( repr( command_argument))
		items.append( repr( command_argument))
		for item in entry[3:]:
			items.append( repr(item))
		items.append( )
		return "(%s)"%( string.join(items, ', '))
	
		
	
	def decomposeCommand( self, command ):
		"""Turn command int+flag into command name + command flag names"""
		flags = []
		for name, value in self.flags:
			if command & value:
				flags.append( name )
				command = command - flag
		for name, value in self.commands:
			if command == value:
				flags.insert(0, name )
				return flags
		raise ValueError( "Unrecognised command integer %s in tag-table (with flags %s)"%(command, flags))
	
