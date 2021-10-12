# How to get the homepage
1. 所有修改结束后，在public中生成目录
    ```bash
    > cd starter-hugo-academic-pzhang/
    > hugo
    ```
2. 上传public到ftp中，将public重新命名成homepage

## How to add a publication
1. 修改 parsers/publication/bibtex_202104_from_cv.bib, 将新的文章的bib添加进去
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

## How to change Editor
```bash
> vi content/{en/zh}/courses/_index.md
```

## How to change Course
```bash
> vi content/{en/zh}/courses/_index.md
```

## How to change CV
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

## How to change photo of pzhang
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

# How to modify a student
1. 删除学生的中文目录和英文目录
    ```bash
    rm -rf ../content/en/authors/Jing-Huang
    rm -rf ../content/zh/authors/Jing-Huang
    ```
2. 修改学生信息或者学生相片
3. 后面的步骤和how to add a student一样。



## Release Notes:
- 20211011: first edition
    - 使用hugo框架，academic模版：github.com/wowchemy/starter-hugo-academic
    - 根据王新民老师提供的一份2015-至今的论文整理，在202104月resume(pzhang_cv_chinese_2016)的publication基础上，添加了新的publication，同时更新了一些abstract
    
