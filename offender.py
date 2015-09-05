#!/usr/bin/env python

import random
import sys


def main(argv):
    s = [None, None, None, None]
    while True:
        command = raw_input('')
        if command == 'quit':
            break
        field = []
        for i in range(0, 4):
            s[i] = raw_input('')
            field.extend(s[i].split())

        fillable = False
        for number in field:
            if int(number) == 0:
                fillable = True
                break

        if not fillable:
            sys.stderr.write('Not Fillable')
            return 1

        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if int(field[x + y * 4]) == 0:
                print "%d %d 2" % (x, y)
                break
        sys.stdout.flush()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
