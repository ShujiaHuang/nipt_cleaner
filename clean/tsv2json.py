"""
Author: Shujia Huang
Date  : 2016-07-27
"""
# -*- coding: utf-8 -*-
import re
import argparse
import json
import sys

from utils import is_number

def tsv2json():
    usage = 'python %prog tsv2json -i infile.tsv > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('tsv2json')
    optp.add_argument('-i', '--infile', dest='infile',
                      help = 'The input file or from STDIN.')
    optp.add_argument('-c', '--column', dest='col',
                      help = 'The column feature')
    optp.add_argument('--pretty', action='store_true', default=False,
                      dest='is_out_pretty', help = 'output json pretty')
    opt = optp.parse_args()

    if not opt.infile or not opt.col:
        pass

    pretty_outdata = []
    key = [s.lower() for s in opt.col.split(',')]
    with open(opt.infile) if opt.infile else sys.stdin as fh:
        for r in fh:
            col = r.strip().split('\t')

            if len(col) < 1 or col[0][0] == '#' or col[1] == 'SAMPLE_NUM':
                continue

            tmp_dict = {key[i]: v if not is_number(v) else float(v)
                        for i, v in enumerate(col)}
            """
            tmp_dict = {key[i]: v for i, v in enumerate(col)}
            """

            if opt.is_out_pretty:
                pretty_outdata.append(tmp_dict)
            else:
                print json.dumps(tmp_dict, ensure_ascii=False)

    if opt.is_out_pretty:
        print json.dumps(pretty_outdata, ensure_ascii=False,
                         indent=4, sort_keys=True)

