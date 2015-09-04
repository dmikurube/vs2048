#!/usr/bin/env python

import random
import sys


directions = ["north", "south", "east", "west"]


def main(argv):
    s = [None, None, None, None]
    while True:
        command = raw_input('')
        if command == 'quit':
            break
        for i in range(0, 4):
            s[i] = raw_input('')
        print directions[random.randint(0, 3)]
        sys.stdout.flush()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
