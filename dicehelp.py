_HELP_STRINGS = [
("""You can quit this help at any time by just typing in "done" above.

    Let's start with a simple case.  You need to roll two d4, three d6, and add 5 it it all.
_______________________""", "2d4 + 3d6 + 5"),
("""I do understand subtraction, multiplication, and order of operations using parentheses.
_______________________""", "5d8 * (d4 + 10)"),
("""I can take an arbitrary number of sides, so a d9 is perfectly valid.

    Expandable rolls: 3x2d9 will become 2d9 + 2d9 +2d9, which is, yes, the same as 6d6, but it's just another way of writing it that I will will accept.

    More useful for that: separated rolling if you need to, say, roll a d20 three times, but separately, and add 15 to them.
_______________________""", "{3xd20} + 15"),
("""You'll notice that it will give you the results of each roll separately.

    This should get you going.  Have fun rolling!
_______________________""", "") ]

def dice_help():
    """This will manage the interactive help as a generator. It yields
    strings.
    """
    for help_str in _HELP_STRINGS:
        yield help_str
