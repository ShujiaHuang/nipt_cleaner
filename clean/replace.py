"""
Author: Shujia Huang
Date  : 2016-07-26
"""
import re
import argparse

NUM_RE = re.compile(r"[\d']+")

def replace():
    usage = 'python %prog replace -t target_input -q query_input -c column > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('replace')
    optp.add_argument('-t', '--target', dest='target',
                      help = 'The target input.')
    optp.add_argument('-q', '--query', dest='query',
                      help = 'The query input.')
    optp.add_argument('-c', '--column', dest='column', type=int,
                      help = 'The replace column.', default=1)

    opt = optp.parse_args()
    target = {}
    with open(opt.target) as f:
        for r in f:
            col = r.strip().split()
            if len(col) == 2:
                target[col[0]] = col[1]

    with open(opt.query) as f:
        for r in f:
            col = r.strip().split()
            if len(col) < opt.column:
                continue

            if col[0][0] == '#':
                print '\t'.join(col)
                continue

            if col[opt.column-1] in target:
                col[opt.column-1] = target[col[opt.column-1]]
            else:
                col[opt.column-1] = 'null'

            print '\t'.join(col)

