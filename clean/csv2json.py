"""
Author: Shujia Huang
Date : 2016-11-17
"""
import sys
import argparse
import csv
import json

#reload(sys)
#sys.setdefaultencoding('utf-8')

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
        title = reader.fieldnames

        if len(colnames) == 0:
            colnames = set([c.upper() for c in title])

        for row in reader:
            try:
                csv_rows = {str.lower(title[i]):unicode(row[title[i]], 'utf-8')
                            for i in range(len(title)) if title[i] in colnames}
            except UnicodeDecodeError:
                print >> sys.stderr, '[WARNING] UnicodeDecodeError', row
                continue

            if opt.is_out_pretty:
                pretty_outdata.append(tmp_dict)
            else:
                print json.dumps(csv_rows, ensure_ascii=False)

    if opt.is_out_pretty:
        print json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)


#Read CSV File
def read_csv(file, colname, format):

    data = []
    colnames = set([c.upper() for c in colname.split(',')])
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames

        if len(colnames) == 0:
            colnames = set([c.upper() for c in title])

        for row in reader:
            try:
                csv_rows = {str.lower(title[i]):unicode(row[title[i]], 'utf-8')
                            for i in range(len(title)) if title[i] in colnames}
            except UnicodeDecodeError:
                print >> sys.stderr, '[WARNING] UnicodeDecodeError', row
                continue

            if format=='pretty':
                data.append(csv_rows)
            else:
                print json.dumps(csv_rows, ensure_ascii=False)

    if format=='pretty':
        print json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
