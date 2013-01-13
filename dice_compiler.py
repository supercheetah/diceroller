import sys
if 'kivy.logging' not in sys.modules.keys():
    import logging
else:
    from kivy.logger import Logger
from collections import deque
from rollenum import *

XOR = lambda x, y: (not x and y) or (not y and x)
ADDER_PUSH = lambda adder, x: adder.insert(0, x)
ISLAMBDA = lambda l: isinstance(l, type(lambda: None)) and l.__name__ == '<lambda>'

def compile_log(mesg):
    """Emit compile log messages.
    
    Arguments:
    - `mesg`:
    """
    if 'kivy.logging' not in sys.modules.keys():
        logging.debug(mesg)
    else:
        Logger.debug('Compiler: ' + mesg)

def negate_adder( adder ):
    return multiply_adder( adder, -1 )

def multiply_adder( adder, multiplier ):
    mult_adder = []
    for i in adder:
        if isinstance(i, int):
            mult_adder.append(multiplier*i)
        else:
            mult_adder.append(str(-int(multiplier*i)))
    return mult_adder

def prod_deque( multiplier, coef ):
    new_mult = deque([])
    # This is a boolean.
    divide = multiplier[1]
    compile_log("prod_deque(): multiplier={0}, coef={1}".format(multiplier, coef))
    for i in multiplier[0]:
        m = 1/float(i[0]) if divide else float(i[0])
        if isinstance(i[0], int):
            new_mult.append(coef*m)
        else:
            new_mult.append(str(coef*m))
    return new_mult

def product( multiplier ):
    if 1==len(multiplier):
        return multiplier.pop()
    assert 0<=len(multiplier), "This is a bad error. We shouldn't get here. Please report this: multiplier=%s" % (str(multiplier))
    prod = 1.0
    is_const = True
    compile_log("product(): multiplier=" + str(multiplier))
    for i in multiplier:
        if not isinstance(i[0], deque):
            compile_log("\ti of multiplier={0}, is int={1}". \
                            format(str(i), str(isinstance(i[0], int))))
            # i[1] tells us if we need to divide or not.
            m = 1/float(i[0]) if i[1] else float(i[0])
            prod *= m
            # It's a constant if it's given to us as a string.
            if isinstance(i[0], int):
                is_const = False
        else:
            return prod_deque(i, prod)
    return (str(prod) if is_const else prod)

def generate_adder( bytecode ):
    # Throw all the numbers in here and do the addition later.
    adder = deque([])
    # Just turn subtraction into addition to make our lives easier.
    negate = False
    # Are we dividing by this number? Division is treated as
    # multiplication where n/x == n*1/x.
    divide = False
    # For any multiplication we encounter, we must solve right away.
    multiplier = deque([])
    # This is where we create the string to give back to the user.
    eqn_str = ''
    # Dump all the constant group strings here. The counter counts
    # them for identification.
    const_grp_strings = []
    const_counter = 0
    # A bit hackish to overcome Python shortcomings, but it works for
    # what I want.
    const_add_string = lambda cstr: 0 if \
        const_grp_strings.append(cstr) else const_counter+1
    # Resets negate back to false, may be used to reset other vars in
    # the future.
    reset = lambda: False
    logdebug = lambda: compile_log(eqn_str + '\n\tadder:\t'+str(adder) + \
                                       '\n\tmult:\t'+str(multiplier))
    add_to_adder = lambda data: adder.append(data[0]) if \
        isinstance(data[0], deque) else adder.appendleft(data[0])
    for instruction in bytecode:
        # This is such an ugly function.  I'm just not sure there is a
        # way to break it up into more functions.  That's not
        # completely true.  It's just that without pass by reference,
        # I can't see it, at least not in a way that would be clean or
        # elegant.
        if instruction.opFn == Fn.constant:
            eqn_str += str(instruction.data)
            data = -instruction.data if negate else instruction.data
            multiplier.appendleft((str(data), divide))
            negate = reset()
            logdebug()
        elif instruction.opFn == Fn.const_grouping:
            ((const_str, subconst_str, constant), is_neg) = instruction.data()
            for sub_str in subconst_str:
                const_counter = const_add_string(sub_str)
            const_counter = const_add_string(const_str)
            if is_neg:
                eqn_str += '-'
            eqn_str += '[({0}): {1}]'.format(const_counter, constant)
            data = -constant if XOR(negate, is_neg) else constant
            multiplier.appendleft((str(data), divide))
            negate = reset()
            logdebug()
        elif instruction.opFn == Fn.dice:
            dice_str, dice_sum = instruction.data.sum(negate)
            eqn_str += dice_str
            multiplier.appendleft((dice_sum, divide))
            negate = reset()
            logdebug()
        elif instruction.opFn == Fn.xdice:
            x_str, expansion = instruction.data.expand(negate)
            eqn_str += x_str
            multiplier.appendleft(expansion.popleft())
            data = product(multiplier)
            # We're done multiplying, so we need an empty multiplier
            multiplier = deque([])
            add_to_adder(data)
            while 1<len(expansion):
                adder.appendleft(expansion.popleft())
            if 0!=len(expansion):
                # If some weirdo decides to use 1xd?, this won't work
                # since expansion will be empty.
                multiplier.append((expansion.pop(), divide))
            negate = reset()
            logdebug()
        elif instruction.opFn == Fn.var_grouping:
            is_neg = instruction.data.pop()
            var_str, var_const_grp_str, var_adder = generate_adder(instruction.data)
            if var_const_grp_str:
                const_add_string(var_const_grp_str)
            if XOR(negate, is_neg):
                var_adder = negate_adder(var_adder)
            if is_neg:
                eqn_str += '-('+var_str+')'
            else:
                eqn_str += '('+var_str+')'
            instruction.data.append(is_neg)
            multiplier.append((var_adder, divide))
            negate = reset()
            logdebug()
        elif instruction.opFn == Fn.op:
            eqn_str += ' '+OpsRepr[instruction.data]+' '
            if instruction.data == Ops.sub:
                negate = True
            if instruction.data == Ops.div:
                divide = True
            # As soon as we encounter any non-multiplication operator,
            # clear out multiplier. For our purposes, division is the
            # same as multiplication.
            if instruction.data in (Ops.sub, Ops.add):
                data = product(multiplier)
                # We're done multiplying, so we need an empty multiplier.
                multiplier = deque([]) 
                add_to_adder(data)
                divide = False
            logdebug()
    # We need to clean up after ourselves, and clear out the
    # multiplier.
    logdebug()
    if 0<len(multiplier):
        data = product(multiplier)
    if isinstance(data, deque):
        adder.append(data)
    else:
        adder.appendleft(data)
    logdebug()
    return eqn_str, const_grp_strings, adder

def add_up( num_array, addition ):
    _sum = 0
    const_adder = 0
    add_later = 0
    for i in num_array:
        if isinstance( i, int ) or isinstance( i, float ):
            _sum += i + addition
        elif isinstance( i, str ):
            const_adder += float(i)
        else:
            _sum += const_adder
            # add_later is the sum of the constants inside the
            # sub-list
            _sum, add_later = add_up( i, _sum )
            _sum += add_later
    return _sum, const_adder

def dice_compile( bytecode ):
    eqn_str, const_grp_strings, adder = generate_adder(bytecode)
    last = adder[len(adder)-1]
    if not isinstance(last, deque):
        # This takes care of the corner case where there are no
        # var_groupings
        adder.append([0])
    answer, garbage = add_up(adder, 0)
    compile_log("answer: "+str(answer))
    return eqn_str, const_grp_strings, answer
