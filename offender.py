#!/usr/bin/env python

import random
import sys


def main(argv):
    s = [None, None, None, None]
    while True:
        command = raw_input('')
        if command == 'quit':
            break
        for i in range(0, 4):
            s[i] = raw_input('')
        print "%d %d 2" % (random.randint(0, 3), random.randint(0, 3))
        sys.stdout.flush()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
