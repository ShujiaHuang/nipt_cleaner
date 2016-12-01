"""
Author: Shujia Huang
Date  : 2016-07-13 17:43:50
"""
# -*- coding: utf-8 -*-
import sys
import time
import argparse
import json


def listfeature():
    from clean.listfeature import listfeature
    listfeature()


def extraction():
    from clean.extract import extraction_feature
    extraction_feature()


def extract_million():
    from clean.extract_million import extraction_feature
    extraction_feature()


def extract_million_HPV():
    from clean.extract_million_HPV import extraction_feature
    extraction_feature()


def idmap():
    from clean.id_map import id_map
    id_map()


def replace_element():
    from clean.replace import replace
    replace()


def combine():
    from clean.combine import combine_information
    combine_information()


def tsv2json():
    from clean.tsv2json import tsv2json
    tsv2json()


def csv2json():
    from clean.csv2json import csv2json
    csv2json()


if __name__ == '__main__':
    runner = {'list': listfeature,
              'extraction': extraction,
              'extraction_million': extract_million,
              'extraction_million_HPV': extract_million_HPV,
              'id_map': idmap,
              'replace': replace_element,
              'combine': combine,
              'tsv2json': tsv2json,
              'csv2json': csv2json}
    if len(sys.argv) == 1 or (sys.argv[1] not in runner):
        print >> sys.stderr, '[Usage] python [option] %s' % sys.argv[0]
        print >> sys.stderr, '\n\t'.join(['Option:'] + runner.keys())
        sys.exit(1)

    command = sys.argv[1]
    runner[command]()

    print >> sys.stderr, '** %s ALL DONE %s **' % (command, time.asctime())
    print >> sys.stderr, '>> For the flowers bloom in the desert <<'




