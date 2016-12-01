"""
Author: Shujia Huang
Date  : 2016-07-27
"""
# -*- coding: utf-8 -*-
import re
import argparse
import json

from utils import is_number

# empty value in Chinese 
EMPTY_VALUE = u'\u7a7a\u503c'

def load_config(conf_file):
    """
    """
    infiles = []
    with open(conf_file) as f:
        for r in f:
            r = r.strip()
            if len(r) == 0 or r[0] == '#': continue
            col = r.split()
            infiles.append([col[1], col[0].split(',')])

    return infiles


def combine_information():
    usage = 'python %prog combine --conf d.conf > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('combine')
    optp.add_argument('-c', '--conf', dest='conf',
                      help = 'The configuration file')
    optp.add_argument('--pretty', action='store_true', default=False,
                      dest='is_out_pretty', help = 'output json pretty')
    opt = optp.parse_args()
    in_files = load_config(opt.conf)

    data = {}
    feature_set = set()
    for file, keys in in_files:

        _ = [feature_set.add(k) for k in keys]

        with open(file) as fh:
            for r in fh:
                col = r.strip().split()
                if len(col) > 0 and col[0][0] != '#':

                    # Main ID
                    if col[0] not in data:
                        data[col[0]] = {}

                    tmp_dict = {}
                    for i, k in enumerate(keys):
                        if i < len(col):
                            col[i] = col[i].decode('utf-8')
                            col[i] = 'null' if col[i] == EMPTY_VALUE else col[i]
                            tmp_dict[k] = (col[i].encode('utf-8') 
                                           if not is_number(col[i]) else float(col[i]))

                        else:
                            tmp_dict[k] = 'null'

                    data[col[0]].update(tmp_dict)

    pretty_outdata = []
    for i, (k, v) in enumerate(data.items()):
        for feat in feature_set:
            if feat not in v:
                v[feat] = 'null'

        # rename the sample id
        # v['sample_id'] = i + 1

        if 'trisomy' in v and v['trisomy'] == 'null':
            v['trisomy'] = 'normal'

        if 'validation' in v and v['validation'] == 'null':
            v['validation'] = 'normal'

        if opt.is_out_pretty:
            pretty_outdata.append(v)
        else:
            print json.dumps(v, ensure_ascii=False)

    if opt.is_out_pretty:
        print json.dumps(pretty_outdata, ensure_ascii=False,
                         indent=4, sort_keys=True)


