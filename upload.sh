#!/bin/bash
#date
#filepath=/Users/huangjing/Documents/1.项目/5.网站维护/starter-hugo-academic-pzhang/public

DATE


lftp << EOF
open ftp://Zhangpw:pku_01_zhangpw@162.105.94.3
cd private
rm -rf homepage_old
mirror -R public homepage_new
mv homepage homepage_old
mv homepage_new homepage
close
bye
EOF

DATE
echo 'Finish'
