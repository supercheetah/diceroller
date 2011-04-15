#!/bin/bash

PYDIR="c:/Python27"
PYTHON="wine $PYDIR/python.exe"
WINPWD=`winepath -w \`pwd\``

cd pyinstaller

$PYTHON Configure.py
$PYTHON Makespec.py -p $WINPWD $WINPWD/diceroller.py
$PYTHON Build.py diceroller/diceroller.spec