# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 bianlifeng.com, Inc, All Rights Reserved
#
"""
@File:  doc2bib.py 
@Author: jing.huang02
@Date: 2021/10/6 下午8:06 
@Description: 
@Changelist:
- 1.0 first edition
@article {name1,
author = {作者, 多个作者用 and 连接},
title = {标题},
journal = {期刊名},
volume = {卷20},
number = {页码},
year = {年份},
}
demo line:
142.	Yin, Jianyuan; Wang, Yiwei; Chen, Jeff Z. Y.; Zhang, Pingwen; Zhang, Lei; Construction of a Pathway Map on a Complicated Energy Landscape, Phys. Rev. Lett., 2020, 124(9).
"""
import sys
import re

def form_first_line(value):
    return '@article {{{},\n'.format(value)

def form_last_line():
    return '}\n'

def form_line(key, value):
    if value is None:
        value = ''
    if isinstance(value, list):
        if key != 'author':
            raise ValueError('Invalid key {} and value {}'.format(key, value))
        else:
            v = [v.strip() for v in value]
            return '{} = {{{}}},\n'.format(key, ' and '.join(v))
    return '{} = {{{}}},\n'.format(key, value)

def parse_author(desc):
    values = desc.split(' and ')
    if len(values) == 1:
        authors = [desc.split(',')[0]]
        desc = ','.join(desc.split(',')[1:])
    else:
        v1 = values[0].split(',')
        v2 = ' and '.join(values[1:])
        authors = v1 + [v2.split(',')[0]]
        desc = ','.join(v2.split(',')[1:])
    return authors, desc

def parse_next(desc, c):
    values = desc.split(c)
    v = [v.strip() for v in values[1:]]
    return values[0].strip(), c.join(v)

def parse_title(desc):
    return parse_next(desc, ',')

def parse_journal(desc):
    return parse_next(desc, ',')


def parse_volume_number_page(desc):
    volume = None
    number = None
    page = None
    # 解析vol
    match_obj = re.search('[Vv]ol[^0-9]*([0-9]*)', desc)
    if match_obj:
        volume = match_obj.group(1)
    match_obj = re.search('No[^0-9]*([0-9]*)', desc)
    if match_obj:
        number = match_obj.group(1)
    # 解析page
    match_obj = re.search('([0-9]*-[0-9]*)', desc)
    if match_obj:
        page = match_obj.group()
    if volume is None and number is None:
        match_obj = re.search('([0-9]*)[\s]*\(([0-9]{1,3})\)', desc)
        if match_obj:
            volume = match_obj.group(1)
            number = match_obj.group(2)
    return (volume, number, page, desc)

def parse_year(desc):
    res = re.search('\((\d{4})\)', desc)
    return res.group(1), ''


def parse_line(line):
    line = line.strip()
    id = line.split('.')[0]
    desc = '.'.join(line.split('.')[1:]).strip()
    # parse author
    authors, desc = parse_author(desc)
    # parse title
    title, desc = parse_title(desc)
    # parse journal
    #print('EED', desc)
    journal, desc = parse_journal(desc)
    # parse volumn,
    #print('EEE', desc)
    volume, number, page, desc = parse_volume_number_page(desc)
    #print('EEF', desc)
    # parse year
    year, desc = parse_year(desc)

    first_line = form_first_line(id)
    author = form_line('author', authors)
    title = form_line('title', title)
    journal = form_line('journal', journal)
    year = form_line('year', year)
    volume = form_line('volume', volume)
    number = form_line('number', number)
    page = form_line('page', page)
    last_line = form_last_line()
    return first_line + author + title + journal + year + volume + number + page + last_line
    #return first_line + author + title + journal + year + volume + last_line


if __name__ == '__main__':
    usage = 'doc2bib.py filename'
    if len(sys.argv) != 2:
        print(usage)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip()
            if len(l) > 0:
                try:
                    out_l = parse_line(l)
                    print(out_l)
                except Exception as e:
                    print(l)
                    raise e
