#!/bin/sh

# This is to be used with fsniper

PID=`cat kivymain.pid`

if [ -e /proc/$PID -a /proc/$PID/exe ]; then
    kill -9 $PID
fi

python main.py & echo $! > kivymain.pid
