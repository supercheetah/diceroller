import logging
import random
import compiler
from dispexcept import VarNestedException, VarMultipleException
from rollenum import *
from simpleparse.dispatchprocessor import *
from rollil import *
#from simpleparse.error import ParserSyntaxError

def get_const_strings():
    if is_separated():
        return Lexer.constGrpStrings
    else:
        return Lexer.sepConstGrpStrings

def get_sep_grp_results():
    return Lexer.sepGrpStrings, Lexer.sepGrpResults

def get_resolution():
    return Lexer.eqnString, Lexer.resolution

def is_separated():
    return Lexer.isSeparated

class Lexer( DispatchProcessor ):
    _insideVarGroup = False
    _varGroupCount = 0

    constGrpStrings = []

    sepGrpStrings = []
    sepGrpResults = []
    sepConstGrpStrings = []

    resolution = 0
    eqnString = ""

    isSeparated = False
    
    def roll( self, (tag,start,stop,subtags), buffer ):
        """The start of processing a 'roll.'  Forms the root of the tree."""
        logging.debug("def:      roll")
        logging.debug("tag:     "+str(tag))
        logging.debug("start:   "+str(start))
        logging.debug("stop:    "+str(stop))
        logging.debug("subtags: "+str(subtags))
        logging.debug("buffer:  "+str(buffer)+"\n")
        for tup in subtags:
            if "space" == tup[0]:
                continue
            try:
                result = dispatch( self, tup, buffer)
            except SyntaxError, se:
                raise se
        logging.debug("result:  "+str(result)+'\n')

    def init_var( self ):
        self._insideVarGroup = False
        self._varGroupCount = 0
        Lexer.constGrpStrings = []
        Lexer.sepGrpStrings = []
        Lexer.sepGrpResults = []
        Lexer.isSeparated = False
        
    def root_fn( self, (tag,start,stop,subtags), buffer ):
        """This is where all the magic happens."""
        self.init_var()
        logging.debug("def:            root_fn")
        try:
            result = dispatch( self, subtags[0], buffer )
        except SyntaxError, se:
            raise se
        logging.debug("root result:   "+str(result)+'\n')
        final = compiler.compile( result )
        Lexer.eqnString, Lexer.constGrpStrings, Lexer.resolution = final
        return final

    def operations( self, (tag,start,stop,subtags), buffer ):
        """The start of a new roll equation"""
        logging.debug("def:            operations")
        logging.debug("tag:           "+str(tag))
        logging.debug("start:         "+str(start))
        logging.debug("stop:          "+str(stop))
        logging.debug("subtags:       "+str(subtags))
        logging.debug("buffer:        "+str(buffer))
        logging.debug("subtags[0]:    "+str(subtags)[0]+"\n")
        try:
            result = dispatch( self, subtags[0], buffer)
        except SyntaxError, se:
            raise se
        logging.debug("operations result:")
        logging.debug("\t"+str(result)+'\n')
        return result


    def function( self, (tag,start,stop,subtags), buffer ):
        """This contains the actual operations"""
        logging.debug("def:         function")
        logging.debug("tag:        "+str(tag))
        logging.debug("start:      "+str(start))
        logging.debug("stop:       "+str(stop))
        logging.debug("subtags:    "+str(subtags))
        logging.debug("buffer:     "+str(buffer))
        logging.debug("subtags[0]: "+str(subtags[0])+'\n')
        bytecode = []
        for tup in subtags:
            if "space" == tup[0]: #We don't need to do anything for a space.
                continue
            try:
                result = dispatch( self, tup, buffer)
            except SyntaxError, se:
                raise se
            if "operations" == tup[0]:
                bytecode.extend(result)
                logging.debug('  opfn:'+str(bytecode)+'\n')
            elif "grouping" == tup[0]:
                bytecode.append(result)
                logging.debug(' grpfn:'+str(bytecode)+'\n')
            else:
                bytecode.append(RollInstruction(StrFn(tup[0]),result))
                logging.debug('   '+str(tup[0])+':',result)
                logging.debug('    bytecode:'+str(bytecode)+'\n')
        logging.debug("")
        return bytecode


    def constant( self, (tag,start,stop,subtags), buffer ):
        """Returns a number to the tree"""
        logging.debug("def:         constant")
        logging.debug("tag:        "+str(tag))
        logging.debug("start:      "+str(start))
        logging.debug("stop:       "+str(stop))
        logging.debug("subtags:    "+str(subtags))
        logging.debug("buffer:     "+str(buffer))
        logging.debug("subtags[0]: "+str(subtags)+"\n")
        try:
            return dispatch( self, subtags[0], buffer )
        except SyntaxError, se:
            raise se


    def grouping( self, (tag,start,stop,subtags), buffer ):
        """Begins the processing of a group of operations"""
        try:
            return dispatch( self, subtags[0], buffer )
        except SyntaxError, se:
            raise se

    def var_grouping( self, (tag,start,stop,subtags), buffer ):
        """Operations outside of this group apply to each inside (except constants),
        which is then added up to the whole.  There can be only one var_grouping per
        roll equation, and nesting is not allowed."""
        if self._insideVarGroup:
            #raise Exception("Cannot nest variable groupings")
            raise VarNestedException( start )
        if self._varGroupCount > 0:
            #raise Exception("Cannot have more than one variable grouping")
            raise VarMultipleException( start )
        logging.debug("def:        var_grouping")
        logging.debug("tag:       "+str(tag))
        logging.debug("start:     "+str(start))
        logging.debug("stop:      "+str(stop))
        logging.debug("subtags:   "+str(subtags))
        result = None
        is_negative = False 
        self._insideVarGroup = True
        for tup in subtags:
            if "space" == tup[0]:
                continue # Why waste processing power on spaces?
            if "negation" == tup[0]:
                is_negative = True
                continue
            if "operations" != tup[0]:
                raise Exception("How can there be anything other than an operation here?!")
            try:
                result = dispatch( self, tup, buffer)
            except SyntaxError, se:
                raise se
        result.append(is_negative)
        self._insideVarGroup = False
        self._varGroupCount += 1
            
        return RollInstruction(Fn.var_grouping, result)

    def const_grouping( self, (tag,start,stop,subtags), buffer ):
        """Operations inside this group are processed first, and return a single constant."""
        # Since everything in a const_grouping gets processed right away, we don't care about these until we're done.
        save_inside_var_grp = self._insideVarGroup
        save_var_grp_count = self._varGroupCount
        self._insideVarGroup = False
        self._varGroupCount = 0
        
        negation = False
        for tup in subtags:
            if "space" == tup[0]:
                continue
            if "negation" == tup[0]:
                negation = True
                continue
            if "operations" != tup[0]:
                raise Exception("How can there be anything other than an operation here?!")
            try:
                bytecode = dispatch ( self, tup, buffer )
            except SyntaxError, se:
                raise se
        solution = lambda x=bytecode: (compiler.compile( bytecode ), negation)
        ## future thought for separated constants (a different grammar element):
        ## solution = lambda x=bytecode: compiler.compile( bytecode )
        #if negation:
        #    solution = -solution
        #Lexer.constGrpStrings.append(eqn_str)
        # We're done!  Set them back to what they were before.
        self._insideVarGroup = save_inside_var_grp
        self._varGroupCount = save_var_grp_count
        return RollInstruction( Fn.const_grouping,  solution )

    def sep_grouping( self, (tag,start,stop,subtags), buffer ):
        """This is a group of rolls that should all be taken separately.  Returns a list of rolls."""
        Lexer.isSeparated = True
        die_type = 'd'
        rolls = None
        is_neg = False
        bytecode = []
        for tup in subtags:
            if "space" == tup[0]:
                continue
            try:
                result = dispatch( self, tup, buffer )
            except SyntaxError, se:
                raise se
            if "xdice" == tup[0]:
                rolls = result
            elif "op" == tup[0]:
                bytecode.append(RollInstruction(Fn.op, result))
            else:
                bytecode.extend(result)

        bytecode.insert(0, RollInstruction( Fn.dice, rolls.rollIteration ))
        logging.debug("sep_dice:")
        for i in range(rolls.numRolls):
            self._insideVarGroup = False # These need to be reset for each roll
            self._varGroupCount = 0
            eqn_str, const_grp_strings, answer = compiler.compile(bytecode)
            Lexer.sepGrpStrings.append(eqn_str)
            Lexer.sepGrpResults.append(answer)
            Lexer.sepConstGrpStrings.append(const_grp_strings)

    def rollit( self, (tag,start,stop,subtags), buffer ):
        """Common function to both dice and sep_dice.  Does not sum the rolls.
        Returns die type as a string, and the rolls, as lambda expressions, not
        the result.  The value is determined when it is needed."""
        num_dice = 1
        dice_sides = 0
        include_zero = False
        for tup in subtags:
            try:
                result = dispatch(self, tup, buffer)
            except SyntaxError, se:
                raise se
            if tup[0] == "num_dice":
                num_dice = result
            elif tup[0] == "incl_zero":
                include_zero = result
            else:
                dice_sides = result
        die_type = "d"+str(dice_sides)
        start = 1
        if include_zero:
            die_type = "D"+str(dice_sides)
            start = 0
        logging.debug("dice_sides:    "+str(dice_sides))
        logging.debug("num_dice:      "+str(num_dice))
        logging.debug("include_zero:  "+str(include_zero))
        if include_zero:
            start = 0
        roll_fn = lambda x=0: random.randint(start, dice_sides)+x
        is_negative = num_dice<0 and True or False
        return DiceRoll(is_negative, die_type, roll_fn, abs(num_dice))

    def dice( self, (tag,start,stop,subtags), buffer ):
        """This defines the actual dice being rolled"""
        # This started out with different logic from sep_dice. Things change though.
        # Originally this did the rolling of the dice, and their summation, but then
        # I realized it was better to do that only when it was needed.
        logging.debug("def:            dice")
        logging.debug("tag:           "+str(tag))
        logging.debug("start:         "+str(start))
        logging.debug("stop:          "+str(stop))
        logging.debug("subtags:       "+str(subtags))
        logging.debug("buffer:        "+str(buffer))
        logging.debug("rolls:")
        return self.rollit( (tag,start,stop,subtags), buffer )

    def sep_dice( self, (tag,start,stop,subtags), buffer ):
        """This defines the actual dice being rolled, but not added together.
        Returns the die type, and a list of rolls."""
        logging.debug("def:            sep_dice")
        logging.debug("tag:           "+str(tag))
        logging.debug("start:         "+str(start))
        logging.debug("stop:          "+str(stop))
        logging.debug("subtags:       "+str(subtags))
        logging.debug("buffer:        "+str(buffer))
        logging.debug("")
        return self.rollit( (tag,start,stop,subtags), buffer )

    def xdice( self, (tag,start,stop,subtags), buffer ):
        """This will expand an expression, so '6x3d6' becomes '3d6+3d6+3d6',
        and returns it as a list.  sep_dice already does most of this work for us.
        For negated rolls, I consider '-6x3d6' and '6x-3d6' to be equivalent.
        Double negation makes it positive."""
        logging.debug("def:            xdice")
        logging.debug("tag:           "+str(tag))
        logging.debug("start:         "+str(start))
        logging.debug("stop:          "+str(stop))
        logging.debug("subtags[0]:    "+str(subtags[0]))
        logging.debug("subtags[1]:    "+str(subtags[1]))
        logging.debug("buffer:        "+str(buffer))
        num_rolls = dispatch( self, subtags[0], buffer ) #This will call number
        logging.debug("num_rolls:     "+str(num_rolls))
        try:
            rollset = dispatch( self, subtags[1], buffer) #This will call sep_dice
        except SyntaxError, se:
            raise se
        expanded_rolls = ExpandedRoll(rollset, num_rolls)
        return expanded_rolls

    def num_dice( self, (tag,start,stop,subtags), buffer ):
        """Number of dice being rolled"""
        try:
            return dispatch( self, subtags[0], buffer )
        except SyntaxError, se:
            raise se

    def num_sides( self, (tag,start,stop,subtags), buffer ):
        """Number of sides on the dice"""
        try:
            return dispatch( self, subtags[0], buffer )
        except SyntaxError, se:
            raise se

    def incl_zero( self, (tag,start,stop,subtags), buffer ):
        """If this is a capital 'D', include zero."""
        try:
            return "D"==buffer[start]
        except SyntaxError, se:
            raise se

    def op( self, (tag,start,stop,subtags), buffer ):
        """This defines the operations being used (at this time, plus and minus)"""
        logging.debug("def:         op")
        logging.debug("tag:        "+str(tag))
        logging.debug("start:      "+str(start))
        logging.debug("stop:       "+str(stop))
        logging.debug("subtags:    "+str(subtags))
        logging.debug("buffer:     "+str(buffer))
        logging.debug("subtags[0]: "+str(subtags[0])+"\n")
        try:
            space_start, op_position = dispatch( self, subtags[0], buffer)
        except SyntaxError, se:
            raise se
        ops_assoc = {'+':Ops.add, '-':Ops.sub, '*':Ops.mul, '/':Ops.div}
        return ops_assoc[buffer[op_position]]

    def number( self, (tag,start,stop,subtags), buffer ):
        """returns the number"""
        return int(buffer[start:stop])

    def space( self, (tag,start,stop,subtags), buffer):
        """Return the start, and the end."""
        return start,stop
