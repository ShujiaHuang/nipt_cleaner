"""
Author: Shujia Huang
Date  : 2016-07-26
"""
import re
import argparse

NUM_RE = re.compile(r"[\d']+")

def id_map():
    usage = 'python %prog id_map -t target_input -q query_input > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('id_map')
    optp.add_argument('-t', '--target', dest='target',
                      help = 'The target input.')
    optp.add_argument('-q', '--query', dest='query',
                      help = 'The query input.')

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
            if len(col) == 0:
                continue

            if col[0] in target:
                col[0] = target[col[0]]
                if len(col) == 1:
                    col.append('null')
                else:
                    #tmp = NUM_RE.findall(col[1])
                    #col[1] = int(tmp[0]) if len(tmp) else 'null'
                    pass

                print '\t'.join(map(str, [col[0]] + col[1:]))

