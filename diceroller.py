#!/usr/bin/env python
import traceback
import sys
import rollparse
import os
import logging
if 'posix' == os.name:
    import readline
import cli_args

def main():
    if 'posix' == os.name:
        readline.parse_and_bind('set editing-mode vi')
    while True:
        try:
            eqn_str = raw_input("Roll it! ('q' to quit): ")
        except EOFError:
            break
        
        if '' == eqn_str:
            continue

        if 'q' == eqn_str[0]:
            break

        try:
            const_strings = []
            ans_str = []
            answers = None
            is_separated, const_strings, (ans_str, answers) = rollparse.solve_roll(eqn_str)
        except Exception as e:
            print e
            #print sys.exc_traceback.tb_lineno
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                logging.debug("Error in %s on line %d" % (fname, lineno))
            continue

        if 0 < len(const_strings) and not is_separated:
            print "Calculated constants:"
            i = 1
            for c in const_strings:
                print "  {0}: {1}".format(i, c)
                i += 1

        if is_separated:
            print "Rolls:"
            for i in range(0,len(ans_str)):
                const_counter = 1
                for const_str in const_strings[i]:
                    print "    [{0}: {1}]".format(const_counter, const_str)
                    const_counter += 1
                print "  {0}: {1} = {2}".format(i+1, ans_str[i], answers[i])
        else:
            print "{0} = {1}".format(ans_str, answers)

    return 0

if __name__ == "__main__":
    if cli_args.dice_args.debug:
        logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
