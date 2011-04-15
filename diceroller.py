#!/usr/bin/python
import sys
import rollparse
import os
if 'posix' == os.name:
    import readline

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
            is_separated, const_strings, (ans_str, answers) = rollparse.solve_roll(eqn_str)
        except Exception as e:
            print e
            continue

        if 0 < len(const_strings):
            print "Calculated constants:"
            i = 1
            for c in const_strings:
                print "  {0}: {1}".format(i, c)
                i += 1

        if is_separated:
            print "Rolls:"
            for i in range(len(ans_str)):
                print "  {0}: {1} = {2}".format(i+1, ans_str[i], answers[i])
        else:
            print "{0} = {1}".format(ans_str, answers)

    return 0

if __name__ == "__main__":
    sys.exit(main())
