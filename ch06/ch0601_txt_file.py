# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0601_txt_file.py
@Version    :   v0.1
@Time       :   2019-12-20 16:01
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0601，P162
@Desc       :   数据加载、存储与文件格式，读写文本格式的数据
@理解：
"""
import json
# common imports
import sys
from datetime import datetime
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
import winsound
from pandas import DataFrame, Series

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# P162，表6-1：Pandas中的解析函数
# 1. read_csv：从文件、URL、文件型对象中加载带有分隔符的数据。默认分隔符为逗号
# 2. read_table：从文件、URL、文件型对象中加载带有分隔符的数据。默认分隔符为制表符（\t）
# 3. read_fwf：读取定宽列格式数据（即没有分隔符）
# 4. read_clipboard：读取剪贴板中的数据。默认分隔符为制表符（\t）
# 以上函数的参数：
# 1. 索引：将一个或者多个列当作返回的DataFrame处理
# 2. 类型推断和数据转换：包括用户定义值的转换、缺失值的标记列表等
# 3. 日期解析：单个日期解析和组合多个列的日期解析
# 4. 迭代：对大文件进行逐块迭代
# 5. 不规整数据处理：跳过一些行、页脚、注释或者其他一些不需要的东西。

# python console: !type ch06\\ex1.csv
def ch0601000_read_data():
    data = pd.read_csv('ch06/ex1.csv')
    print('-' * 5, "使用 read_csv 读取的原始数据", '-' * 5)
    pp(data)

    data = pd.read_table('ch06/ex1.csv', sep = ',')
    print('-' * 5, "使用 read_table 读取的原始数据", '-' * 5)
    pp(data)

    data = pd.read_csv('ch06/ex2.csv', header = None)
    print('-' * 5, "没有标题的原始数据", '-' * 5)
    pp(data)

    names = ['a', 'b', 'c', 'd', 'message']
    data = pd.read_csv('ch06/ex2.csv', names = names)
    print('-' * 5, "有标题的原始数据", '-' * 5)
    pp(data)

    data = pd.read_csv('ch06/ex2.csv', names = names, index_col = 'message')
    print('-' * 5, "有标量和索引的原始数据", '-' * 5)
    pp(data)

    data = pd.read_csv('ch06/csv_mindex.csv', index_col = ['key1', 'key2'])
    print('-' * 5, "多重索引的原始数据", '-' * 5)
    pp(data)

    pp(list(open('ch06/ex3.txt')))
    data = pd.read_table('ch06/ex3.txt', sep = '\s+')
    print('-' * 5, "使用正则表达式读取原始数据", '-' * 5)
    pp(data)  # read_table 推断第一列为索引
    pp(data.sort_index(ascending = False))

    # !type ch06\\ex5.csv
    data = pd.read_csv('ch06/ex5.csv')
    print('-' * 5, "使用 read_csv 读取有缺失值的原始数据", '-' * 5)
    pp(data)

    data = pd.read_csv('ch06/ex5.csv', na_values = ['world'])
    print('-' * 5, "设置原始数据中的默认缺失值", '-' * 5)
    pp(data)

    sentinels = {'message': ['world', 'NA'], 'something': ['three']}
    data = pd.read_csv('ch06/ex5.csv', na_values = sentinels)
    print('-' * 5, "设置原始数据中的默认缺失值", '-' * 5)
    pp(data)


# ch060101. 逐块读取文本文件
def ch060101_read_pieces():
    data = pd.read_csv('ch06/ex6.csv')
    print('-' * 5, "ex6.csv 原始数据", '-' * 5)
    pp(data)

    data = pd.read_csv('ch06/ex6.csv', nrows = 5)
    print('-' * 5, "指定行数读取原始数据", '-' * 5)
    pp(data)

    chunk_data = pd.read_csv('ch06/ex6.csv', chunksize = 1000)
    pp(chunk_data)
    data = Series([])
    for piece in chunk_data:
        data = data.add(piece['key'].value_counts(), fill_value = 0)
        pass
    print('-' * 5, "指定块大小读取原始数据", '-' * 5)
    pp(data)


# ch060102. 将数据写出到文本格式
def ch060102_write_txt_file():
    data = pd.read_csv('ch06/ex5.csv')
    print('-' * 5, "ex5.csv 原始数据", '-' * 5)
    pp(data)
    data.to_csv('ch06/ex5_out.csv')  # 输出会增加索引列
    data.to_csv(sys.stdout, sep = '|')  # 分隔符
    data.to_csv(sys.stdout, na_rep = 'NULL')  # 空字符串的填充
    data.to_csv(sys.stdout, index = False, header = False)  # 索引输出和标题输出
    data.to_csv(sys.stdout, index = False)
    data.to_csv(sys.stdout, index = False, columns = ['a', 'b', 'c'])  # 选择需要输出的列

    # Series 的 from_csv, to_csv 方法
    dates = pd.date_range(start = datetime(2000, 1, 1), periods = 7)
    data = Series(np.arange(7), index = dates)
    data.to_csv(sys.stdout)

    # Series.from_csv() 已经被废弃


# ch060103. 手工处理分隔符格式
def ch060103_delimited_formats():
    # !type ch06\\ex7.csv
    import csv

    f = open('ch06/ex7.csv')
    reader = csv.reader(f)
    for line in reader:
        print(line)
        pass

    lines = list(csv.reader(open('ch06/ex7.csv')))
    header, values = lines[0], lines[1:]
    data_dict = {h: v for h, v in zip(header, zip(*values))}
    pp(data_dict)

    # P172，表6-3：csv.Dialect 类的选项
    # 1. delimiter：用于分隔字段的单字符字符串。默认为“,”
    # 2. lineterminator：用于写操作的行结束符。默认为“\r\n”。可以帮助读取跨平台的文本
    # 3. quotechar：用于带有特殊字符（如分隔符）的字段的引用符号。默认为“"”
    # 4. quoting：引用约定。
    #   - csv.QUOTE_ALL：引用所有字段
    #   - csv.QUOTE_MINIMAL：引用带有诸如分隔符之类特殊字符的字段。（默认）
    #   - csv.QUOTE_NONNUMERIC：引用非数字
    #   - csv.QUOTE_NONE：不引用
    # 5. skipinitialspace：忽略分隔符后面的空白符。默认为 False
    # 6. doublequote：字段内的引用符号的处理。True则双写。
    # 7. escapechar：用于对分隔符进行转义的字符串。默认禁用。
    class my_dialect(csv.Dialect):
        lineterminator = '\n'
        delimiter = ','
        quotechar = '"'
        quoting = csv.QUOTE_NONNUMERIC
        pass

    with open('ch06/mydata.csv', 'w') as f:
        writer = csv.writer(f, dialect = my_dialect)
        writer.writerow(('one', 'two', 'three'))
        writer.writerow((1, 2, 3))
        pass


# ch060104. JSON 数据
def ch060104_json():
    obj = """
    {"name":"Wes",
    "places_lived":["United States","Spain","Germany"],
    "pet":null,
    "siblings":[{"name":"Scott","age":25,"pet":"Zuko"},
                {"name":"Katie","age":33,"pet":"Cisco"}]
    }
    """
    data = json.loads(obj)
    print('-' * 5, "将json格式转换为Python格式", '-' * 5)
    pp(data)

    data_json = json.dumps(data)
    print('-' * 5, "将Python格式转换为json格式", '-' * 5)
    pp(data_json)

    siblings = DataFrame(data['siblings'], columns = ['name', 'age'])
    pp(siblings)
    pp(siblings.to_json())


# ch060105. XML和HTML：Web信息收集。
# ToDo：因为需要网站，而国外网站读取不到，并且速度很慢，就放弃了。
def ch060105_web_txt():
    from lxml.html import parse
    from urllib.request import urlopen

    parsed = parse(urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options'))
    doc = parsed.getroot()
    links = doc.findall('.//a')
    pp(links[15:20])

    lnk = links[28]
    pp(lnk)
    pp(lnk.get('href'))
    pp(lnk.text_content())

    urls = [lnk.get('href') for lnk in doc.finall('.//a')]
    pp(urls[-10:])
    pass


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
