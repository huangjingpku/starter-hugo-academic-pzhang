# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 bianlifeng.com, Inc, All Rights Reserved
#
"""
Receives a Bibtex file and produces the markdown files for academic-hugo theme
@author: Petros Aristidou
@contact: p.aristidou@ieee.org
@date: 19-10-2017
@version: alpha
@adapted by Tobias Gerstenberg
@date: 11-21-2017
It would be nice to adapt the parser in the future so that it creates the long publication in APA style. Maybe using: https://docs.pybtex.org/
python3 parse_bib_cic.py -i static/bibtex/cic_papers.bib
"""

import bibtexparser
import os, sys, getopt, shutil
from citation_generator import construct_citation
import datetime
from xpinyin import Pinyin


# 资源所在目录
SRC_DIR='../static/publication/'


# It takes the type of the bibtex entry and maps to a corresponding category of the academic theme
# Publication type.
# Legend:
# 0 = Uncategorized;
# 1 = Conference paper;
# 2 = Journal article;
# 3 = Preprint / Working Paper;
# 4 = Report;
# 5 = Book;
# 6 = Book section;
# 7 = Thesis;
# 8 = Patent\n''')
PUBTYPE_DICT = {
    'forthcoming': '"0"',
    'uncategorized': '"0"',
    'preprint': '"3"',
    'article': '"2"',
    'inproceedings': '"1"',
    'incollection': '"6"',
    'thesis': '"7"'
}


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

def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


# You can add the name of a co-author and their website and it will create a link on the publications website
# useless
def get_author_link(string):
    web = {
        # 'T. Gerstenberg':'https://tobiasgerstenberg.github.io/'
    }
    out = ''
    try:
        out = web[string]
    except:
        pass
        #print("Author's " + string + " website is missing.")
    return out

def get_pinyin(v):
    # TODO: 拼音转换
    p = Pinyin()
    return p.get_pinyin(v).split('-')

def generate_id(title, year, lang = 'en'):
    # process year
    if year.strip() == '':
        raise ValueError('Empty year. Please use this year instead')
    try:
        year = int(year)
    except ValueError as e:
        raise e
    this_year = datetime.datetime.now().year
    if year > this_year:
        raise ValueError('{} must before this year {}'.format(year, this_year))

    # process title
    if lang == 'en':
        trim_words = ['of', 'on', 'in', 'for', 'with', 'a', 'and', 'or', 'to', 'the', 'an', 'at', 'via', 'by', 'from']
        vs = []
        for v in title.lower().split():
            if v not in trim_words:
                vs.append(v)
        title_value = (''.join([v[0] for v in vs])).upper()


    elif lang == 'zh':
        vs = get_pinyin(title)
        title_value = [v[0] for v in vs if len(v) > 0 and v[0].isalpha()]
        title_value = ''.join(title_value).upper()


    return str(year) + '_' + title_value



def write_title(entry, the_file):
    the_file.write(
        '''# Publication type.
        # Legend: 
        # 0 = Uncategorized; 
        # 1 = Conference paper; 
        # 2 = Journal article;
        # 3 = Preprint / Working Paper; 
        # 4 = Report; 
        # 5 = Book; 
        # 6 = Book section;
        # 7 = Thesis; 
        # 8 = Patent\n''')
    the_file.write('title = "' + supetrim(entry['title']) + '"\n')


def write_date(entry, the_file):
    if 'year' in entry:
        yr = entry['year']
        if RepresentsInt(yr):
            date = yr
            if 'month' in entry:
                if RepresentsInt(entry['month']):
                    month = entry['month']
                else:
                    month = str(month_string_to_number(entry['month']))
                date = date + '-' + month.zfill(2)
            else:
                date = date + '-01'
            the_file.write('date = "' + date + '-01"\n')
        else:
            dt = datetime.datetime.now()
            date = str(dt.year) + '-' + str(dt.month).zfill(2) + '-' + str(dt.day).zfill(2)
            the_file.write('date = "' + date + '"\n')
            the_file.write('year = "' + yr + '"\n')
    else:
        dt = datetime.datetime.now()
        date = str(dt.year) + '-' + str(dt.month).zfill(2) + '-' + str(dt.day).zfill(2)


def write_author(entry, the_file):
    # Treating the authors
    if 'author' in entry:
        authors = entry['author'].split(' and ')
        the_file.write('authors = [')
        authors_str = ''
        for author in authors:
            author_strip = supetrim(author)
            #author_split = author_strip.split(',')
            #if len(author_split) == 2:
            #    author_strip = author_split[1].strip() + ' ' + author_split[0].strip()
            #author_split = author_strip.split(' ')

            # print(author_strip, author_split, entry['ID'])
            #author_strip = author_split[0][0] + '. ' + ' '.join(map(str, author_split[1:]))
            #author_web = get_author_link(author_strip)
            #if author_web:
            #    authors_str = authors_str + '"[' + author_strip + '](' + author_web + ')",'
            authors_str = authors_str + '"' + author_strip + '",'
        the_file.write(authors_str[:-1] + ']\n')


def write_publication_type(entry, the_file):
    # Treating the publication type
    if 'ENTRYTYPE' in entry:
        pub_type_entry = 'publication_types = [' + PUBTYPE_DICT[entry['ENTRYTYPE']] + ']\n'
        if 'year' in entry:
            if not RepresentsInt(entry['year']):
                pub_type_entry = pub_type_entry.replace('[', '[' + PUBTYPE_DICT['forthcoming'] + ', ')

        the_file.write(pub_type_entry)

    else:
        the_file.write('publication_types = [' + pubtype_dict[entry['uncategorized']] + ']\n')

def write_publication_short(entry, the_file):
    if 'booktitle' in entry:
        the_file.write('publication_short = "' + supetrim(entry['booktitle']) + '"\n')
    elif 'journal' in entry:
        the_file.write('publication_short = "' + supetrim(entry['journal']) + '"\n')
    elif 'school' in entry:
        the_file.write('publication_short = "' + supetrim(entry['school']) + '"\n')
    elif 'institution' in entry:
        the_file.write('publication_short = "' + supetrim(entry['institution']) + '"\n')

        # I never put the short version. In the future I will use a dictionary like the authors to set the acronyms of important conferences and journals
        # Not sure what the above comment is about. This adds the citation to the markdown file


def write_publication(entry, the_file):
    the_file.write('publication = ' + construct_citation(entry) + '\n')


def write_abstract(entry, the_file):
    if 'abstract' in entry:
        the_file.write('abstract = "' + abstract_trim(supetrim(entry['abstract'])) + '"\n')

def write_doi(entry, the_file):
    if 'doi' in entry:
        the_file.write('doi = "' + supetrim(entry['doi']) + '"\n')

def write_link(entry, the_file):
    if 'link' in entry:
        the_file.write('url_pdf = "'+supetrim(entry['link'])+'"\n')


def get_note_value(note_str, key):
    vs = note_str.split(',')
    for v in vs:
        k, value = v.split(':')
        if k == key:
            return value
    return None


def write_selected(entry, the_file):
    if 'note' in entry:
        value = get_note_value(entry['note'], 'featured')
        if value in ['true', 'false']:
            the_file.write('featured = {}\n'.format(value))
        else:
            raise ValueError('Invalid feature value [{}] in [{}]'.format(value, entry['note']))
        value = get_note_value(entry['note'], 'category')
        the_file.write('categories = ["{}"]\n'.format(value))
    else:
        the_file.write('featured = false\n')

def write_config(entry, the_file):
    the_file.write('math = true\n')
    the_file.write('highlight = true\n')


def copy_file(src_file, dst_file, tag = 'PDF'):
    if os.path.exists(src_file):
        shutil.copyfile(src_file, dst_file)
        sys.stderr.write('-- Generate {} Successful: {} from {}\n'.format(tag, dst_file, src_file))
    else:
        sys.stderr.write('-- Generate {} Failed: Can not find {}\n'.format(tag, src_file))
        # double check
        if tag == 'PDF':
            emp_file = src_file.replace('.pdf', '.emp')
            if not os.path.exists(emp_file):
                sys.stderr.write('-- Find EMP Failed: Can not find empty file {}. Please check spelling mistakes\n'.format(emp_file))



def parse_command(argv):
    inputfile = ''
    lang = 'en'
    output_lang = ''
    try:
        opts, args = getopt.getopt(argv, "hi:l:o:", ["ifile="])
    except getopt.GetoptError:
        print('parse_bib.py -i <inputfile> -l <lang> -o <outputdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('parse_bib.py -i <inputfile>')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-l"):
            lang = arg
        elif opt in ("-o"):
            output_lang = arg
    if output_lang == 'en':
        outputdir = '../content/en/publication/'
    elif output_lang == 'zh':
        outputdir = '../content/zh/publication/'
    else:
        outputdir = './'

    return inputfile, lang, outputdir


if __name__ == "__main__":
    inputfile, lang, outputdir = parse_command(sys.argv[1:])
    try:
        with open(inputfile, encoding="utf8") as bibtex_file:
            bibtex_str = bibtex_file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print('File ' + inputfile + ' not found or some other error...')
        exit(2)


    bib_database = bibtexparser.loads(bibtex_str)

    # loop over entries
    for entry in bib_database.entries:
        id = generate_id(entry['title'], entry['year'], lang)
        filedir = '{}/{}/'.format(outputdir, id)
        filenm = '{}/index.md'.format(filedir)
        pdf_src = '{}/{}.pdf'.format(SRC_DIR, id)
        pdf_dst = '{}/{}.pdf'.format(filedir, id)
        img_src = '{}/{}.jpg'.format(SRC_DIR, id)
        img_dst = '{}/featured.jpg'.format(filedir, id)

        # If the same publication exists, then skip the creation. I customize the .md files later, so I don't want them overwritten. Only new publications are created.
        if os.path.exists(filedir):
            sys.stderr.write('Existed [{}] for [{}], Skip\n'.format(filedir, entry['title']))
        else:
            sys.stderr.write('Generate DIR [{}] for [{}]\n'.format(filedir, entry['title']))
            os.makedirs(filedir)
            with open(filenm, 'w', encoding="utf8") as the_file:
                the_file.write('+++\n')
                write_title(entry, the_file)
                write_date(entry, the_file)
                write_author(entry, the_file)
                write_publication_type(entry, the_file)
                write_publication_short(entry, the_file)
                write_publication(entry, the_file)
                write_abstract(entry, the_file)
                write_doi(entry, the_file)
                write_link(entry, the_file)
                write_config(entry, the_file)
                # by default ,selected = false
                write_selected(entry, the_file)
                the_file.write('+++')
                sys.stderr.write('-- Generate FILE Successful: [{}] \n'.format(filenm))
                copy_file(img_src, img_dst, 'IMG')
                copy_file(pdf_src, pdf_dst, 'PDF')




