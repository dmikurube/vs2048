#!/usr/bin/env python

import fcntl
import os
import subprocess
import sys

from nbstreamreader import NonBlockingStreamReader as NBSR


def initialField():
    return [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 2, 0, 0,
        0, 0, 0, 2,
        ]


def printField(field, out):
    for index, number in enumerate(field):
        out.write('%d ' % number)
        if index > 0 and index % 4 == 3:
            out.write('\n')
    out.flush()


def slide(field, direction):
    return field


def place(field, put):
    (x, y, num) = put.split()
    field[int(x) + int(y) * 4] = int(num)
    return field


count = 0
def gameover(field):
    global count
    count = count + 1
    if count > 20:
        return True
    return False


def main(argv):
    field = initialField()
    offender = []
    defender = []

    pos = None
    for arg in argv:
        if arg == '-o':
            pos = 'offender'
        elif arg == '-d':
            pos = 'defender'
        elif pos == 'offender':
            offender.append(arg)
        elif pos == 'defender':
            defender.append(arg)

    if len(offender) == 0 or len(defender) == 0:
        print "no args"
        return 1

    offender_proc = subprocess.Popen(offender,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=False)
    offender_in = offender_proc.stdin
    offender_out = NBSR(offender_proc.stdout)

    defender_proc = subprocess.Popen(defender,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=False)
    defender_in = defender_proc.stdin
    defender_out = NBSR(defender_proc.stdout)

    while True:
        printField(field, sys.stdout)

        defender_in.write('game\n')
        printField(field, defender_in)
        direction = defender_out.readline(0.1)
        print direction,

        field = slide(field, direction)
        if gameover(field):
            break

        offender_in.write('game\n')
        printField(field, offender_in)
        put = offender_out.readline(0.1)
        print put,

        field = place(field, put)
        if gameover(field):
            break

    offender_in.write('quit\n')
    defender_in.write('quit\n')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
