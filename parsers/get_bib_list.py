# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 bianlifeng.com, Inc, All Rights Reserved
#
"""
Receives a Bibtex file and produces the publication list for resume
Using format:
J. D. Bryngelson, J. N. Onuchic, N. D. Socci, and P. G.Wolynes,
Funnels pathways and the energy landscape ofprotein folding: A synthesis,
Proteins 21, 167 (1995).
Authors,title, publication, Volumn, Number, (year).

"""

import bibtexparser
import os, sys, getopt, shutil
from citation_generator import construct_citation
import datetime



def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def supetrim(string):
    return string.replace("\\", "").replace("{", "").replace("}", "").replace("\n", " ")


def abstract_trim(string):
    return string.replace('"', "\\\"")


def get_journal(entry):
    return supetrim(entry['journal'])


def get_title(entry):
    return supetrim(entry['title'])


def get_year(entry):
    return '({}).'.format(supetrim(entry['year']))


def get_author(entry):
    # Treating the authors
    if 'author' in entry:
        authors = entry['author'].split(' and ')
        authors_str = ','.join(authors[0:-1])
        if authors_str == '':
            return authors[-1]
        else:
            return '{} and {}'.format(authors_str, authors[-1])


def get_volumne_number(entry):
    vol_str = ''
    num_str = ''
    if 'volume' in entry and supetrim(entry['volume']) != '':
        vol_str = 'Vol. ' + supetrim(entry['volume'])
    if 'number' in entry and supetrim(entry['number']) != '':
        num_str = 'No. ' + supetrim(entry['number'])
    return vol_str + ', ' + num_str

def get_page(entry):
    page_str = ''
    if 'page' in entry and supetrim(entry['page']) != '':
        page_str = supetrim(entry['page'])
    return page_str

def get_note_value(note_str, key):
    vs = note_str.split(',')
    for v in vs:
        k, value = v.split(':')
        if k == key:
            return value
    return None


def if_selected(entry, the_file):
    if 'note' in entry:
        value = get_note_value(entry['note'], 'featured')
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise ValueError('Invalid feature value [{}] in [{}]'.format(value, entry['note']))
    else:
        return False


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('get_bib_list.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('get_bib_list.py -i <inputfile>')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    return inputfile


def get_citation(entry):
    author = get_author(entry)
    title = get_title(entry)
    journal = get_journal(entry)
    vol_num = get_volumne_number(entry)
    year = get_year(entry)
    page = get_page(entry)
    return ', '.join([author, title, journal, vol_num, page, year])


if __name__ == "__main__":
    inputfile = main(sys.argv[1:])
    try:
        with open(inputfile, encoding="utf8") as bibtex_file:
            bibtex_str = bibtex_file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print('File ' + inputfile + ' not found or some other error...')
        exit(2)


    bib_database = bibtexparser.loads(bibtex_str)

    # loop over entries
    index = 1
    for entry in bib_database.entries[::-1]:
        line = get_citation(entry)
        line = '{}. {}'.format(index, line)
        index = index + 1
        print(line)
