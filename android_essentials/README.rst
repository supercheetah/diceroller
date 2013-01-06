=============================
A Better Dice Rolling Program
=============================

:Author: Rene Horn
:Homepage: <https://github.com/supercheetah/diceroller>

Every dice rolling program I've encountered has a number of annoying
limitations or quirks, and this is to address them.  What I've written
here allows for actual equations to be written for dice rolls of any
arbitrary number of sides.  It will be best to illustrate by example,
so read on.

(You might notice that this is an unfinished readme.)

Examples
========

So, let's say you need to roll 4d6 (that's four six-sided dice) and
add two to the total.  This is the easy case that can be entered into
the program::

  4d6 + 2

This should give you something like the following::

  (d6: 3 + 4 + 2 + 2) + 2 = 13

Notice that it gives you the numbers for each of the d6 rolls so you
can see what it actually rolled.

Now, let's say, however that there's a call for four d6 rolls, but not
added together, and two needs to be added to each roll::

  {4xd6} + 2

The part with ``{4xd6}`` is called a `Separation Group`_.  What this
will return is something like the following::

  Rolls:
    1: (d6: 5) + 2 = 7
    2: (d6: 5) + 2 = 7
    3: (d6: 4) + 2 = 6
    4: (d6: 6) + 2 = 8

We are certainly not limited to six sided dice here either.  Any
positive number after the ``d`` will signify the number of sides that
need to be on a die.  Another scenario that could happen is if there
were a call for a roll of a d6 and a d8 with two added to both, and
then that added for the total (yes, you could add four to the total
and get the same result, but I'm just trying to make a point here).
For that we can use a `Variable Group`_ in something like this::

  (d6 + d8) + 2

This is not your typical math equation here, so don't just roll a d6
and a d8 and then add two.  That's not what's going to happen.  The
return from this equation will result in something like the
following::

  ((d6: 1) + (d8: 4)) + 2 = 9

Notice that the only way to get the nine here is to add the two to one
and four separately, and then add up those two sums.

One thing to note is that with ``variable groups`` is that constants
are not factored into the list of terms that get added to that which
is outside, so take the following example::

  (3d4 + 2d10 + 5) + d6

The above will return something like this::

  ((d4: 2 + 3 + 2) + (d10: 6 + 9) + 5) + (d6: 3) = 33

So notice that in order to get 33, three needs to be added to the d4
rolls and to the d10 rolls, and those two sums get added together and
then the five gets added (as a math equation, it would look like (7 +
3) + (15 + 3) + 5 for an example).

What if there is a need for a random constant?  There are precedence
operators (or, as I call them, a `Constant Group`_) that force what's
within to be calculated immediately::

  (3d4 + 2d8 + [5d6 - 10d4]) + d10

This will return something akin to the following::

    1: (d6: 2 + 2 + 4 + 2 + 6) - (d4: 4 + 1 + 3 + 2 + 2 + 2 + 2 + 2 + 4 + 2)
  ((d4: 4 + 2 + 1) + (d8: 8 + 3) + [1: -8]) + (d10: 9) = 28

(Again, remember that terms outside of the ``variable group`` do not
get added to constants inside the variable group.)

Also, there is a bit of a short cut if there is a need to write
``2d6+2d6+2d6``, which can be represented as thus in this example::

  (3x2d6) + 4

This is the same as the following::

  (2d6 + 2d6 + 2d6) + 4

And so both will result in something like the following::

  ((d6: 5 + 2) + (d6: 3 + 3) + (d6: 4 + 3)) + 4 = 32

Operations
==========

At the moment, there are only two operations--addition and
subtraction.  I do plan on adding multiplication and division for
this, but I haven't figured out how I will do that, or what that will
mean with some things.

Dice
====

The dice type always has a ``d`` in it or a ``D``, and there is a
difference.  ``D`` will include ``0`` as one of the sides that is a
part of the roll, where as ``d`` does not include a ``0``.

Immediately preceding a ``d`` is the number of dice that are a part of
a roll, and so, for example, ``2d4`` signifies that two four-sided
dice are being rolled.

If a number and ``x`` immediately precede the dice roll, this is an
expanded roll.  ``3x2d4`` becomes ``2d4+2d4+2d4``.

Note that with an expanded roll, there is always at least one dice
that is a part of the roll, so ``2xd6`` is the equivalent of
``2x1d6``.

Variable Group
==============

A variable group is a set of operations and dice rolls that will be
modified by the terms outside of it.  They are always surrounded by
parentheses.  At this time, they cannot be nested, and there cannot be
more than one (unless it's inside a ``Constant Group``_).

Constant Group
==============

These get calculated immediately, and are always surrounded by square
brackets (``[]``).  In the results, the calculations for the different
constant groups are listed.

Separation Group
================

This allows for multiple, but separate rolls of a dice, and the form
is always in the syntax of an expanded dice surrounded by curly
brackets (``{}``), so ``{3x2d8}`` will result in three separate 2d8
rolls.

Dependencies
============

Python
------

Umm, right, this requires Python.  <http://python.org>

enum.py
-------

This is not my code.  It was written by Ben Finney.  Please see that
file for more information, or go to
<http://pypi.python.org/pypi/enum/>

SimpleParse
-----------

This is dependent on SimpleParse for defining and parsing the grammar.
Please see <http://simpleparse.sourceforge.net/> for more information.

License
=======

I'm distributing this under the Artistic License 2.0.  See COPYING for
details.

Copyright (c) 2011 Rene Horn
