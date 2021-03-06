#!/usr/bin/env python

import os
import subprocess
import signal
import sys
import time

from nbstreamreader import NonBlockingStreamReader as NBSR


def initialField():
    return [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        ]


def placeable(field):
    fillable = False
    for number in field:
        if number == 0:
            return True
    return False


def printField(field, out):
    for index, number in enumerate(field):
        out.write('%d ' % number)
        if index > 0 and index % 4 == 3:
            out.write('\n')
    out.flush()


directions = {
    'north': {
        'start': 0,
        'delta': 4,
        'next': 1,
        },
    'east': {
        'start': 4-1,
        'delta': -1,
        'next': 4,
        },
    'south': {
        'start': 4 * 4 - 1,
        'delta': -4,
        'next': -1,
        },
    'west': {
        'start': 4 * (4 - 1),
        'delta': 1,
        'next': -4,
        },
    }


def slide(oldField, direction):
    field = list(oldField)
    moved = False
    score = 0
    _next = directions[direction]['start']
    delta = directions[direction]['delta']
    for i in range(0, 4):
        to = _next
        _from = _next + delta
        lim = _next + delta * 4
        _next += directions[direction]['next']
        while _from != lim:
            if field[_from] == 0:
                _from += delta
            elif field[to] == 0:
                field[to] = field[_from]
                field[_from] = 0
                _from += delta
                moved = True
            elif field[to] == field[_from]:
                field[to] *= 2
                score += field[to]
                field[_from] = 0
                _from += delta
                to += delta
                moved = True
            else:
                to += delta
                if _from == to:
                    _from += delta

    return moved, field, score


def place(field, put):
    (x, y, num) = put.split()
    if field[int(x) + int(y) * 4] > 0:
        raise "Illegal place."
    field[int(x) + int(y) * 4] = int(num)
    return field


def gameover(field):
    if slide(field, 'north')[0]:
        return False
    if slide(field, 'south')[0]:
        return False
    if slide(field, 'east')[0]:
        return False
    if slide(field, 'west')[0]:
        return False
    return True


def main(argv):
    field = initialField()
    offender = []
    defender = []

    verbose = False
    pos = None
    for arg in argv:
        if arg == '-o':
            pos = 'offender'
        elif arg == '-d':
            pos = 'defender'
        elif arg == '-v':
            verbose = True
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
    offender_pid = offender_proc.pid

    defender_proc = subprocess.Popen(defender,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=False)
    defender_in = defender_proc.stdin
    defender_out = NBSR(defender_proc.stdout)
    defender_pid = defender_proc.pid

    turn = 0
    score = 0
    while True:
        turn += 1
        if verbose:
            print '=== Turn %d (Score: %d) ===' % (turn, score)
            printField(field, sys.stdout)

        offender_in.write('game\n')
        printField(field, offender_in)
        put = offender_out.readline(2.0)
        if verbose:
            print '>> ' + put,

        field = place(field, put)
        if gameover(field):
            break
        if verbose:
            printField(field, sys.stdout)

        defender_in.write('game\n')
        printField(field, defender_in)
        direction = defender_out.readline(2.0)
        if verbose:
            print '>> ' + direction,

        moved, field, plusscore = slide(field, direction.strip())
        score += plusscore
        if not placeable(field):
            break

        if verbose:
            printField(field, sys.stdout)
        if gameover(field):
            break

    offender_in.write('quit\n')
    defender_in.write('quit\n')
    offender_proc.wait()
    defender_proc.wait()
    time.sleep(0.2)
    print 'Score: %d' % score


if __name__ == '__main__':
    sys.exit(main(sys.argv))
