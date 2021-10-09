# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 bianlifeng.com, Inc, All Rights Reserved
#
"""
@File:  html2group.py 
@Author: jing.huang02
@Date: 2021/10/8 下午12:56 
@Description: 
@Changelist:
- 1.0 first edition
"""
import sys
from lxml import etree

def parse_result(text):
    result = text.strip().split('\n')
    result = [r.strip() for r in result]
    ch_name, en_name = result[0].split('|')
    ch_name = ch_name.strip()
    en_name = en_name.strip()
    vs = en_name.split('(')
    if len(vs) > 1:
        en_name = vs[0].strip()
        co_super = vs[1].strip()[0:-1]
    else:
        en_name = en_name
        co_super = ''
    photo_name = en_name.replace(' ','')
    en_name = ' '.join(en_name.split()[::-1])
    year = result[1].strip()
    if len(result) > 2:
        interest = result[2].strip()
    else:
        interest = ''
    return ch_name, en_name, photo_name, year, interest, co_super




if __name__ == '__main__':
    #with open(sys.argv[1]) as f:
    #    doc = f.read()
    #html = etree.HTML(doc)
    parser = etree.HTMLParser(encoding = 'utf-8')
    html = etree.parse(sys.argv[1], parser = parser)
    #result = etree.tostring(tree, pretty_print = True)
    data = html.xpath('//div[@id="groupInfo"]')
    #data = html.xpath('//div[@id="groupInfo"]')
    #data = html.xpath('//div [@id="groupInfo"]/')
    for i in data:
        print(','.join(list(parse_result(i.xpath('string(.)')))))
    #print(html.xpath(''))
