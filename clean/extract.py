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

#reload(sys)
#sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()

from utils import is_number

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
    print '\t'.join(['#'+features[0]] + features[1:])

    data = []
    uniq_id = set()
    with open(opt.infile) if opt.infile else sys.stdin as f:
        for r in f:
            if not len(r.strip()): continue

            jd = json.loads(r.strip())
            jd_dict = {}

            for k, v in jd.items():
                if (v is None) or (v == ""):
                    jd[k] = 'null'

            for x in features:
                if x in jd:
                    try:
                        jd_dict[x] = (jd[x].encode('utf-8')
                                      if not is_number(jd[x]) else int(jd[x]))
                    except ValueError:
                        print >> sys.stderr, '[ERROR]', r.strip(); #sys.exit(1)
                        jd_dict[x] = 'null'
                else:
                    jd_dict[x] = 'null'

            if opt.uniq_id and jd_dict[opt.uniq_id] in uniq_id:
                continue
            if opt.uniq_id:
                uniq_id.add(jd_dict[opt.uniq_id])

            if opt.is_json_out:
                if opt.is_out_pretty:
                    data.append(jd_dict)
                else:
                    print json.dumps(jd_dict, ensure_ascii=False)

            else:
                print '\t'.join(map(str, [jd_dict[k] for k in features]))

    if opt.is_json_out and opt.is_out_pretty:
        print json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)


