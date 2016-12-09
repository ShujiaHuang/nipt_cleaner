"""
Author: Shujia Huang
Date  : 2016-07-13 17:43:50
"""
# -*- coding: utf-8 -*-
import sys
import time
import argparse
import json
import re

from utils import is_number

RE_WEEK = re.compile(r'(\d+)w?\+?(\d?)')
ZU = u'\u65cf'

def nifty_replace(nifty, m):
    p = re.compile(r'nifty(\d+)')
    g = p.match(nifty)
    if m == 2:
        nifty = 'T' + g.group(1)
    elif m == 1:
        nifty = 'normal'
    elif m == '0':
        nifty = 'null'

    return nifty


def nifty_result_replace(nifty_result, m):
    p = re.compile(r'nifty_result_t(\d+)')
    g = p.match(nifty_result)
    if m == 1:
        nifty_result = 'T' + g.group(1)
    elif m == 2:
        nifty_result = 'normal'
    elif m == 0:
        nifty_result = 'null'

    return nifty_result


def extraction_feature():
    usage = 'python %prog extraction [options] inputfile > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('extractionhearingloss')
    optp.add_argument('-i', '--infile', dest='infile',
                      help = 'The input file or from STDIN.')
    optp.add_argument('-u', '--uniq_id', dest='uniq_id',
                      help = 'The feature of this id should be uniq.',
                      default='')
    optp.add_argument('-f', '--feature', dest='feat', metavar = 'STR',
                      help = 'Features to extration. Please separate '
                      'different features by comma.')
    optp.add_argument('--json', action='store_true', default=False,
                      dest='is_json_out', help = 'Ouput by json format')
    optp.add_argument('--pretty', action='store_true', default=False,
                      dest='is_out_pretty', help = 'output json pretty')
    opt = optp.parse_args()

    features = opt.feat.split(',')
    if opt.uniq_id and opt.uniq_id not in features:
        optp.error('[ERROR] "%s" must in "%s"' % (opt.uniq_id, opt.feat))

    # Output header
    if not opt.is_json_out:
        print '\t'.join(['#'+features[0]] + features[1:])

    data = []
    uniq_id = set()
    n_features, flag = [], True
    with open(opt.infile) if opt.infile else sys.stdin as f:
        for r in f:
            if not len(r.strip()): continue

            jd = json.loads(r.strip())
            jd_dict = {}

            for k, v in jd.items():
                if (v is None) or (v == ""):
                    jd[k] = 'null'

            if 'is_report' in jd and jd['is_report'] == '3': continue
            for x in ['id_number', 'father_idnumber', 'mother_idnumber']:
                if x in jd and is_number(jd[x]):
                    jd['id_number'] = jd[x]

            jd['is_carry'] = 0
            for x in features:
                nx = x
                if x in jd:

                    if x == 'id_number':
                        nx = 'native_place'
                        try:
                            jd[x] = str(int(jd[x]))[0:6] if is_number(jd[x]) else jd[x][0:6]
                        except ValueError:
                            print >> sys.stderr, '[WARNING] ValueError: invalid literal for int()', jd[x]
                            jd[x] = 'null'

                    if x == 'customer_nation':
                        nx = 'ethnicity'
                        if len(jd[x]) and jd[x] != 'null' and jd[x][-1] != ZU:
                            jd[x] += ZU

                    if x == 'check_result':
                        nx = 'hpv_type'
                        if 'HPV' not in jd[x]:
                            jd[x] = 'normal'

                    if 'result' in x and '_type' in x:
                        if (jd[x] == '2' or jd[x] == '3') and jd['is_carry'] != 1:
                            jd['is_carry'] = 1

                    jd_dict[nx] = (jd[x].encode('utf-8')
                                   if not is_number(jd[x]) else jd[x])

                else:
                    jd_dict[nx] = 'null'

                if jd_dict[nx] == '-': jd_dict[nx] = 'null'

                if flag:
                    n_features.append(nx)
                    n_features.append('is_carry')

            flag = False
            jd_dict['is_carry'] = jd['is_carry']

            if opt.uniq_id and jd_dict[opt.uniq_id] in uniq_id:
                continue
            if opt.uniq_id:
                uniq_id.add(jd_dict[opt.uniq_id])

            if opt.is_json_out:
                if opt.is_out_pretty:
                    data.append(jd_dict)
                else:
                    try:
                        print json.dumps(jd_dict, ensure_ascii=False)
                    except UnicodeDecodeError:
                        print >> sys.stderr, jd_dict

            else:
                print '\t'.join(map(str, [jd_dict[k] for k in n_features]))

    if opt.is_json_out and opt.is_out_pretty:
        print json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)


