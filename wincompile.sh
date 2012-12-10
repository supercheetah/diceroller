#!/bin/bash

PYDIR="c:/Python27"
PYTHON="wine $PYDIR/python.exe"

#cd pyinstaller

#$PYTHON Configure.py
#$PYTHON Makespec.py ../diceroller.py
#$PYTHON Build.py diceroller/diceroller.spec
$PYTHON pyinstaller/pyinstaller.py diceroller.py
