# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 bianlifeng.com, Inc, All Rights Reserved
#
"""
@File:  parse_group.py 
@Author: jing.huang02
@Date: 2021/10/8 上午10:43 
@Description: 
@Changelist:
- 1.0 first edition
"""
import os, sys, getopt,shutil
import datetime

# 资源所在目录
SRC_DIR='../static/people/'
DST_DIR='./authors/'

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def supetrim(string):
    return string.replace("\\", "").replace("{", "").replace("}", "").replace("\n", " ")


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
def get_author_link(string):
    web = {
        # 'T. Gerstenberg':'https://tobiasgerstenberg.github.io/'
    }
    out = ''
    try:
        out = web[string]
    except:
        print("Author's " + string + " website is missing.")
    return out


def main(argv):
    inputfile = ''
    lang = 'en'
    try:
        opts, args = getopt.getopt(argv, "hi:l:", ["ifile="])
    except getopt.GetoptError:
        print('parse_group.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('parse_bib.py -i <inputfile>')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-l", "--lang"):
            lang = arg
    return inputfile, lang

def generate_id(en_name):
    return '-'.join(en_name.split())

if __name__ == "__main__":
    inputfile, lang = main(sys.argv[1:])
    if lang != 'en' and lang != 'ch':
        raise ValueError('Invalid lang [{}]'.format(lang))

    try:
        with open(inputfile, encoding="utf8") as group_file:
            group_str = group_file.read().split('\n')
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print('File [' + inputfile + '] not found or some other error...')
        sys.exit(2)

    for entry in group_str:
        #- 中文名,英文名,图片名,研究兴趣,共同辅导信息,group信息
        try:
            ch_name, en_name, years, interest, co_super, group = entry.split(',')
        except ValueError:
            sys.stderr.write('Invalid line format {}\n'.format(entry))
            continue
        id = generate_id(en_name)
        interest = interest.replace(':', ' ')

        filedir = '{}/{}/'.format(DST_DIR, id)
        filenm = '{}/_index.md'.format(filedir)

        img_src = '{}/{}.jpg'.format(SRC_DIR, id)
        default_img_src = '{}/nophoto.jpg'.format(SRC_DIR)
        img_dst = '{}/avatar.jpg'.format(filedir)

        if os.path.exists(filedir):
            sys.stdout.write('Existed Author [{}], Skip\n'.format(filedir))
            continue
        else:
            sys.stdout.write('Generate Author [{}]\n'.format(filedir))
            os.makedirs(filedir)
            with open(filenm, 'w', encoding="utf8") as the_file:
                the_file.write('---\n')
                the_file.write(
                    "# Display name\n\n")
                if lang == 'en':
                    the_file.write('title: ' + supetrim(en_name) + '\n')
                else:
                    the_file.write('title: ' + supetrim(ch_name) + '\n')
                the_file.write('user_groups: ["{}"]\n\n'.format(group))
                the_file.write('\n\n')
                the_file.write('organizations:\n')
                the_file.write('- name: {} {}\n\n'.format(years, co_super))
                the_file.write('Interests:\n')
                the_file.write('- {}\n\n'.format(interest))
                the_file.write('---')
                sys.stdout.write('-- Generate Author [{}] Successful\n'.format(filedir))
                default_photonm = '../static/people/nophoto.jpg'

                if os.path.exists(img_src):
                    shutil.copyfile(img_src, img_dst)
                    sys.stdout.write('-- Generate Img from [{}] Successful\n'.format(img_src))
                else:
                    shutil.copyfile(default_img_src, img_dst)
                    sys.stdout.write('-- Generate Img from [{}] Successful\n'.format(default_img_src))
