"""
Author: Shujia Huang
Date : 2016-11-17
"""
import sys
import argparse
import csv
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def csv2json():
    #Get Command Line Arguments
    usage = 'python %prog csv2json -i <path to infile.csv> > Output'
    optp = argparse.ArgumentParser(description=usage)
    optp.add_argument('csv2json')
    optp.add_argument('-i', '--infile', dest='infile',
                      help = 'The input file or from STDIN.')
    optp.add_argument('-c', '--column', dest='col',
                      help = 'The column feature')
    optp.add_argument('--pretty', action='store_true', default=False,
                      dest='is_out_pretty', help = 'output json pretty')
    opt = optp.parse_args()

    pretty_outdata = []
    colnames = set([c.upper() for c in opt.col.split(',')]) if opt.col else set()
    # read CSV file
    with open(opt.infile) if opt.infile else sys.stdin as fh:
        reader = csv.DictReader(fh)
        title = [h.replace(u'\ufeff', '').replace('"', '') for h in reader.fieldnames]

        if len(colnames) == 0:
            colnames = set([c.upper() for c in title])

        for row in reader:
            row = {k.replace(u'\ufeff', '').replace('"', ''):v for k,v in row.items()}
            try:
                csv_rows = {title[i].lower():unicode(row[title[i]], 'utf-8')
                            for i in range(len(title)) if title[i] in colnames}
            except UnicodeDecodeError:
                print >> sys.stderr, '[WARNING] UnicodeDecodeError', row
                continue

            if opt.is_out_pretty:
                pretty_outdata.append(tmp_dict)
            else:

                try:
                    print json.dumps(csv_rows, ensure_ascii=False)
                except UnicodeEncodeError:
                    print >> sys.stderr, '[WARNING] UnicodeDecodeError', csv_rows, '\n', row
                    sys.exit(1)

    if opt.is_out_pretty:
        print json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)


