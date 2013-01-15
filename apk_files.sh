#!/bin/sh
BASEDIR=$(dirname $0)
cd $BASEDIR
rm android_essentials/*.pyo
cp code.py COPYING d100.png d10.png d12.png d20.png d4.png d6.png d8.png d4-loading.png dice_compiler.py dicehelp.py dice.kv diceroller.spec dispatchdebug.py dispexcept.py enum.py eqnstrings.py icon-from-convertico.com.ico icon-from-gimp.ico icon.ico icon.png __init__.py lexer.py main.py parsertest.py README.rst rollenum.py rollil.py rollit.spec rollparse.py varstore.py version android_essentials
