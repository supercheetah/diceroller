_HELP_STRINGS = [
("""You can quit this help at any time by just typing in "done" above.

    Let's start with a simple case.  You need to roll two d4, three d6, and add 5 it it all.
_______________________""", "2d4 + 3d6 + 5"),
("""I do understand subtraction, multiplication, and order of operations using parentheses.  Also, there is a history that is tracked that you can go through with the up and down arrows (or just tap them as you see them on the right side).
_______________________""", "5d8 * (d4 + 10)"),
("""I can take an arbitrary number of sides, so a d9 is perfectly valid.

    You'll also notice that I record a history of all your rolls on the right.  Just tape them to repeat the roll, or use the up and down arrows to go through the history.

    Expandable rolls: 3x2d9 will become 2d9 + 2d9 +2d9, which is, yes, the same as 6d6, but it's just another way of writing it that I will will accept.

    More useful for that: separated rolling if you need to, say, roll a d20 three times, but separately, and add 15 to them.
_______________________""", "{3xd20} + 15"),
("""You'll notice that it will give you the results of each roll separately.

    You can have named rolls if there is a roll you use a lot.  They will show up on the right side.
_______________________""", "damage: {2x2d4} + d6"),
("""Want to do multiple equations at once?  Use the semicolon.
_______________________""", "2d20 + 5; 3d8 + 10"),
("""This will also work with named equations as well.
_______________________""", "magicattack: {2x2d20} + 3; d8*2; 4d4"),
("""This should get you going.  Have fun rolling!
_______________________""", "") ]

def dice_help():
    """This will manage the interactive help as a generator. It yields
    strings.
    """
    for help_str in _HELP_STRINGS:
        yield help_str
