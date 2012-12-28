_HELP_STRINGS = [
"""You can quit this help at any time by just typing in "done" above.

    Let's start with a simple case.  You need to roll two d4, three d6, and add 5 it it all, which would look like this:
    2d4 + 3d6 + 5
_______________________""",
"""Excellent!  (To be perfectly honest, I'm not really paying attention to what you're putting in there, so if you put something else there, that's fine).

    I do understand subtraction, multiplication, and order of operations using parentheses.

    What would it look like if you had to multiply five d8 by d4 + 10?
_______________________""",
"""Here's what I would have put in there:
    5d8 * (d4 + 10)

    I can take an arbitrary number of sides, so a d9 is perfectly valid.

    Expandable rolls: 3x2d6 will become 2d6 + 2d6 +2d6, which is, yes, the same as 6d6, but it's just another way of writing it that I will will accept.

    More useful for that: separated rolling if you need to, say, roll a d20 three times, but separately, and add 15 to them:
    {3xd20} + 15

    Try it (you can also do something like {3x4d4} as well).
_______________________""",
"""You'll notice that it will give you the results of each roll separately.

    This should get you going.  Have fun rolling!
_______________________""" ]

def dice_help():
    """This will manage the interactive help as a generator. It yields
    strings.
    """
    for help_str in _HELP_STRINGS:
        yield help_str
