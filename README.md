# How to deploy project in local environment
0. 安装hugo：hugo v0.87.0+extended
1. 下载项目的最新版本：https://github.com/huangjingpku/starter-hugo-academic-pzhang.git
    - github还保留了一份原始的未修改的代码：https://github.com/huangjingpku/starter-hugo-academic.git
        fork from：https://github.com/wowchemy/starter-hugo-academic.git
    - starter-hugo-academic-pzhang是在starter-hugo-academic的基础上修改而来
2. 下载依赖库：https://github.com/wowchemy/wowchemy-hugo-themes/releases/tag/v5.0.0
3. 修改starter-hugo-academic-pzhang/go.mod 将外部依赖修改成本地依赖（主要解决速度问题），添加replace来解决本地依赖问题
    ```go
    module github.com/wowchemy/starter-hugo-academic
    
    go 1.15
    
    require (
        github.com/wowchemy/wowchemy-hugo-modules/wowchemy-cms/v5 v5.0.0-20210830150813-8b6612e7631c // indirect
        github.com/wowchemy/wowchemy-hugo-modules/wowchemy/v5 v5.0.0-20210830150813-8b6612e7631c // indirect
    )
    // 把外部依赖换成本地依赖
    replace github.com/wowchemy/wowchemy-hugo-modules/wowchemy-cms/v5 => <Your-Dir>/wowchemy-hugo-themes-5.0.0/wowchemy-cms
    replace github.com/wowchemy/wowchemy-hugo-modules/wowchemy/v5 => <Your-Dir>/wowchemy-hugo-themes-5.0.0/wowchemy
    ```
    修改是否成功的验证：
    - 修改前：build之前，需要downloading依赖库
    - 修改后：直接build（注：如果修改前已经build过了，需要先删缓存hugo_cache(/var/folders/0z/9ff5ml9x7dg9brhjp1qqvqgw0000gn/T/hugo_cache)）

# How to modify contents

## How to add a publication
1. 修改 parsers/bibtex_202104_from_cv.bib, 将新的文章的bib添加进去
    - 如果希望文章被展现在selected_publication中，bib文件在note字段注明'featured:true''：
    ```
    @article {146,
    author = {Wei Wang and Lei Zhang and Pingwen Zhang},
    title = {Modeling and Computation of Liquid Crystals
    },
    journal = {Acta Numerica},
    year = {2021},
    volume = {},
    number = {},
    page = {1-89},
    doi = {10.1017/S09624929XXXXXX},
    note = {featured:true},
    abstract = {Liquid crystal is a typical kind of soft matter that is intermediate between crystalline solids and isotropic fluids. The study of liquid crystals has made tremendous progress over the last four decades, which is of great importance on both fundamental scientific researches and widespread applications in industry. In this paper, we review the mathematical models and their connections of liquid crystals, and survey the developments of numerical methods for finding the rich configurations of liquid crystals.},
        }
    }
    ```
2. 将文章的pdf命名为 year_titleCap.pdf，并放入目录 static/publication/中，如果没有pdf，则touch一个空文件:year_titleCap.emp放入目录 static/publication/中
    - year: publish year，如果是preprint，year使用今年
    - titleCap：文章标题单词的首字母（不考虑介词和冠词）
    - eg: 2021年的文章：An Introduction of 2D to 3D Fluid，缩写为2021_I23F.pdf
3. 如果文章有图片，命名为 year_titlecap.jpg，放入目录 static/publication/中。
4. 检查 parsers/parse_bib.py脚本的DST_DIR配置，将配置改成
    ```python
    DST_DIR = '../content/en/publication/'
    ```
5. 使用parse_bib.py生成对应的英文目录和内容，对于新加的文章，程序会在 ../content/en/publication/中新加一个 year_titlecap的目录，里面放有生成好的md文件
    ```bash
    cd parsers
    python parse_bib.py -i bibtex_202104_from_cv.bib
    ```
6. 检查 parsers/parse_bib.py脚本的DST_DIR配置，将配置改成
    ```python
    DST_DIR = '../content/zh/publication/'
    ```
7. 使用parse_bib.py在../content/zh/publicaiton/中生成对应的文章中文目录，
    ```bash
    > cd parsers
    > python parse_bib.py -i bibtex_202104_from_cv.bib
    ```

## How to add a student
1. 修改 parsers/publication/group_202104_from_homepage.csv, 将新的student的信息添加进去，格式为逗号分割的六个字段：
    - 中文名（王小康）
    - 英文名（Xiaokang Wang）
    - 入学年份-毕业年份（2008-2012 or 2021-）
    - 研究方向
    - 合带信息，如果没有，填空（co supervised by Prof Weinan E）
    - 分组信息，必须使用这几种（Current/Graduated Ph.D Students，Current/Graduated Master Students，Current/Graduated Post doc）
2. 添加照片，命名为 Xiaokang-Wang.jpg，放入到 static/people/中
3. 检查 parsers/parse_group.py脚本的DST_DIR配置，将配置改成
    ```python
    DST_DIR = '../content/en/authors/'
    ```
4. 使用parse_group.py生成对应的学生中文目录（../content/zh/authors/）
    ```bash
    cd parsers
    python parse_group.py -i group_202104_from_homepage.csv -l en
    ```
5. 检查 parsers/parse_group.py脚本的DST_DIR配置，将配置改成
    ```python
    DST_DIR = '../content/zh/authors/'
    ```
6. 使用parse_group.py生成对应的学生英文目录（../content/zh/authors/）
    ```bash
    cd parsers
    python parse_group.py -i group_202104_from_homepage.csv -l zh
    ```

## How to add a news
1. 生成模版，建议event信息命名规则：date_event，如20211008_CSIAM
    ```bash
    # 中文
    > hugo new --kind event zh/event/<my-event>
    # 英文
    > hugo new --kind event en/event/<my-event> 
    ```
2. 根据模版修改信息
    ```bash
    > vi content/zh/event/<my-event>/index.md 
    ```
3. 图片命名为featured.jpg，放入到content/{en/zh}/event/<my-event>/中

## How to modify Editor
```bash
> vi content/{en/zh}/courses/_index.md
```

## How to modify Course
```bash
> vi content/{en/zh}/courses/_index.md
```

## How to modify CV
1. 把新的cv放到static/cv/中，建议命名方式 pzhang_{brief}_cv_{chinese/english}_date.pdf
2. 修改markdown文件
    ```bash
    > vi content/{en/zh}/authors/admin/_index.md
    ```
    ```markdown
   {{< icon name="download" pack="fas" >}} Download my Resume:
    - {{< staticref "cv/<my-eng-cv.pdf>" "newtab" >}}English <Resume>{< /staticref >}</Resume>
    - {{< staticref "cv/<my-chi-brief-cv.pdf>" "newtab" >}}Chinese Resume(brief){{< /staticref >}}
    - {{< staticref "cv/<my-chi-cv.pdf>" "newtab" >}}Chinese Resume{{< /staticref >}}
   ```

## How to moidfy photo of pzhang
```bash
mv new_photo.jpg content/{en/ch}/authors/admin/avatar.jpg
```


## How to modify a publicaiton
1. 删除该文章的中文目录和英文目录
    ```bash
    rm -rf ../content/en/publication/2021_I23F
    rm -rf ../content/zh/publicaiton/2021_I23F
    ```
2. 在bib中修改成正确的信息
3. 后面的步骤和how to add a publication一样。

## How to modify a student
1. 删除学生的中文目录和英文目录
    ```bash
    rm -rf ../content/en/authors/Jing-Huang
    rm -rf ../content/zh/authors/Jing-Huang
    ```
2. 修改学生信息或者学生相片
3. 后面的步骤和how to add a student一样。


# How to deploy and debug locally
```bash
cd starter-hugo-academic
hugo server
```
即可在本地http://localhost:1313/查看更新后的内容，支持本地编辑，同步更新

# How to deploy the modified contents online
1. 所有修改结束后，运行命令，即在public中生成了网站内容
    ```bash
    > cd starter-hugo-academic-pzhang/
    > hugo
    ```
2. 上传public到ftp中，将public重新命名成homepage


# When and How to update info
每年9月做一次大的更新，包括如下内容
- publication: 
    - 中文：王新民
    - 英文：research gate/web of science(https://www.webofscience.com/wos/alldb/summary/7a847821-8eb0-443f-9fe9-8ab347eab376-052c4968/relevance/1)
- students: 李英
- title: 刘钊


# 目录结构说明
## 总体结构和说明
```bash
├── LICENSE.md
├── README.md
├── academic.Rproj
├── assets
├── config:配置
├── content:网页内容
├── data
├── exampleSite
├── go.mod
├── go.mod_local
├── go.mod_remote
├── go.sum
├── images
├── netlify.toml
├── parsers：将bib/csv批量处理成hugo需要的目录和md文件
├── resources
├── scripts
├── static：存储资源文件
├── theme.toml
├── update_wowchemy.sh
└── view.sh 
```
## config
config用于保存配置文件
- _default/config.yaml:基本配置
- _default/languages.yaml:语言配置
- _default/menus.yaml:主页菜单配置
    - 在content/home中如果是my-section.md，则在菜单设置的url中，相对应的设置"/#my-section"
    - 如果是新的landing页面，则在菜单设置的url中，设置"new_landing/"
- _default/params.yaml:theme（hea）和fonts设置，配置说明

## static
static是用于存储静态文件的，包括publication，people和cv
- publication/
  - year_title.pdf：文章名，需要根据命名规则，使用bibtex中的title和year得到的名字保持一致
  - year_title.jpg：图片名，需要根据命名规则，使用bibtex中的title和year得到的名字保持一致
  - 占位符问题：如果找不到pdf，需要touch一个year_title.emp作为占位符，这样可以很方便的定位是否有spelling的问题。从2015年开始（包括2015年），paper都做了占位符
  - 命名规则：year_title.pdf
    - year：yyyy，注意：必须早于当前时间，否则无法被展现，因此如果还处于preprint状态，可以考虑填当年
    - title：文章首字母大写，去除介词/冠词，保留数字（如2D，缩写为2）
- people/
  - Xiaokang-Wang.jpg：命名规范：姓首字母和第一个名的首字母
  - no_photo.jpg：默认照片
- cv/
  - 中文breif简历：pzhang_brief_cv_chinese_{update_date}.{pdf/docx}
  - 中文简历：pzhang_cv_chinese_{update_date}.{pdf/docx}
  - 英文简历：pzhang_cv_chinese_{update_date}.{pdf/docx}

## parser
parse用于存储处理脚本，包括将文献/group信息自动转成academic需要的目录结构和文件
文件：
- bibtex_202104_from_cv.bib：paper的bib信息
- group_202104_from_homepage.csv: 学生基本信息，csv文件，格式如下：
  - 中文名（王小康）
  - 英文名（Xiaokang Wang）
  - 入学年份-毕业年份（2008-2012 or 2021-）
  - 研究方向
  - 合带信息，如果没有，填空（co supervised by Prof Weinan E）
  - 分组信息，只能选这几个（Current/Graduated Ph.D Students，Current/Graduated Master Students，Current/Graduated Post doc）
  脚本：
- parse_bib.py：bib信息转成academic需要的目录和文件
- parse_group.py：csv信息转成academic需要的目录和文件

其他：
- doc2bib.py：把publication_202104_from_cv文件转成bib文件的脚本
- html2group.py：把groupList.html网页的信息转成csv文件的脚本
- groupList.html：网站的group页面
- publication_202104_from_cv：202104版本的cv copy下来的publicaiton list

## content
网页的所有信息保存在该目录中
```bash
.
├── en 英文信息
│   ├── admin
│   ├── authors：张老师的个人介绍和所有学生的页面
│   ├── courses：courses的landing主页
│   ├── editors：editors的landing主页
│   ├── event：新闻页面
│   ├── home：首页landing页面
│   ├── post：无用
│   ├── privacy.md
│   ├── publication：publicaiton页面
│   ├── students：students的landing主页
│   ├── terms.md
│   └── test
└── zh 中文信息
    ├── admin
    ├── authors
    ├── courses
    ├── editors
    ├── event
    ├── home
    ├── privacy.md
    ├── publication
    ├── students
    └── terms.md
```
## 参考文档
- wowchemy使用帮助：https://wowchemy.com/docs/
- bibtex：https://blog.csdn.net/itnerd/article/details/112982649
- bibtex支持的field：https://blog.csdn.net/rc_ll/article/details/18730157?utm_source=itdadao&utm_medium=referral
- hugo-academic的一个示例：homepage/public at master · tobiasgerstenberg/homepage
- hugo不完美教程：https://www.jianshu.com/p/5178731599e2
- 用hugo-academic搭建的网站：
  - https://skyao.io/learning/
- B站视频教程：https://www.bilibili.com/video/BV1iA411v7Gi?p=1
  - 加速方法：https://www.bilibili.com/video/BV1iA411v7Gi?p=9
- Google scholar可以批量生成bibtex文件：https://zhuanlan.zhihu.com/p/147796696
- 个人学术网站的文字参考：
  - https://www.sarahcrumpscience.com/
  - https://www.math.ucla.edu/~tao


## Release Notes:
- 20211011: 1.0.0
    - 使用hugo框架，academic模版：github.com/wowchemy/starter-hugo-academic
    - 根据王新民老师提供的一份2015-至今的论文整理，在202104月resume(pzhang_cv_chinese_2016)的publication基础上，添加了新的publication，同时更新了一些abstract
- 20211011： 1.0.1
    - 增加 CSIAM Transactions on Applied Mathematics的编委
    - 根据李英老师提供的学生信息更新学生状态
