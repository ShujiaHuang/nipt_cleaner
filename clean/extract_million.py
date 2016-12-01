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
    elif m == '0' or m == 0:
        nifty = 'null'
    else:
        print >> sys.stderr, '[ERROR] nifty_replace error. Type unmatch', nifty
        sys.exit(1)

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
    optp.add_argument('extraction')
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


            for x in features:
                nx = x
                if x in jd:

                    if x == 'id_card_number':
                        nx = 'native_place'
                        jd[x] = str(int(jd[x]))[0:6] if is_number(jd[x]) else jd[x][0:6]

                    if x == 'customer_nation':
                        nx = 'ethnicity'
                        if len(jd[x]) and jd[x] != 'null' and jd[x][-1] != ZU:
                            jd[x] += ZU

                    if x == 'sample_age': nx = 'age'
                    if x == 'blood_time': nx = 'testing_time'
                    if x == 'foetus_sex': nx = 'fetus_gender'
                    if x == 'foetus_type': nx = 'number_of_fetus'
                    if x == 'ivf_et':
                        nx = 'ivf_symbol'
                        if is_number(jd[x]) and jd[x] == 2:
                            jd[x] = 'null'

                    if x == 'gest_weeks' or x == 'visit_gest_weeks':
                        nx = 'pregnancy_week' if x == 'gest_weeks' else 'gestational_week'
                        if not is_number(jd[x]) and len(jd[x]) and jd[x] != 'null':
                            g = RE_WEEK.match(jd[x])
                            if g:
                                jd[x] = int(g.group(1))
                                if len(g.group(2)):
                                    jd[x] += float(g.group(2)) / 7
                            else:
                                jd[x] = 'null'


                    if x == 'nifty13' or x == 'nifty18' or x == 'nifty21':
                        nx, jd[x] = 'trisomy', nifty_replace(x, jd[x])

                    if (x == 'nifty_result_t13' or x == 'nifty_result_t18' or
                        x == 'nifty_result_t21'):
                        nx, jd[x] = 'validation', nifty_result_replace(x, jd[x])

                    jd_dict[nx] = (jd[x].encode('utf-8')
                                   if not is_number(jd[x]) else jd[x])

                else:
                    jd_dict[nx] = 'null'

                if flag:
                    n_features.append(nx)
            flag = False

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


