"""
Author: Shujia Huang
Date  : 2016-07-13 17:43:50
"""
# -*- coding: utf-8 -*-
import sys
import time
import argparse
import json

from utils import is_number

def listfeature():
    usage = 'python %prog list [-i inputfile] or <STDIN> > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('list')
    optp.add_argument('-i', '--infile', dest='infile',
                      help = 'The input file or from STDIN.')
    opt = optp.parse_args()

    with open(opt.infile) if opt.infile else sys.stdin as f:
        for r in f:
            if not len(r.strip()): continue
            jd = json.loads(r.strip())
            print '\n'.join(sorted(jd.keys()))
            break

