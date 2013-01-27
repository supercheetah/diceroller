import argparse

dice_args_parser = argparse.ArgumentParser()

dice_args_parser.add_argument('-d', '--debug', help='Turn on debugging', action='store_true')

dice_args_parser.add_argument('--size', help='Set the window size for the GUI', action='store')

dice_args = dice_args_parser.parse_args()

if __name__ == "__main__":
    if dice_args.debug:
        print 'debug is on'
    if dice_args.size:
        print "window size: " + dice_args.size
