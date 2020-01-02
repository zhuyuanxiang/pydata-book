# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0704_string.py
@Version    :   v0.1
@Time       :   2019-12-23 18:19
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0704，P17
@Desc       :   数据规整化：清理、转换、合并、重塑，字符串操作
@理解：
"""
# common imports
import re
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from pandas import Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch070401. 字符串对象方法
def ch070401_string_methods():
    # P218，表7-3：Python内置的字符串方法
    # 1. count：返回子串在字符串中的出现次数（非重叠）
    # 2. endswith, startswith：如果字符串以某个后缀结尾（以某个前缀开头），则返回True
    # 3. join：将字符串用途连接其他字符串序列的分隔符
    # 4. index：如果在字符串中找到子串，则返回子串第一个字符所在的位置。如果没有找到，则引发ValueError
    # 5. find：如果在字符串中找到子串，则返回第一个发现的子串的第一个字符所在的位置，如果没有找到，则返回-1
    # 6. rfind：如果在字符串中找到子串，则返回第一个发现的子串的第一个字符所在的位置。如果没有找到，则返回-1
    # 7. replace：用另一个字符串替换指定的子串
    # 8. strip, lstrip, rstrip,：去除空白符（包括换行符）。
    # 9. split：通过指定的分隔符将字符串为一组子串
    # 10. lower, upper：分别将字母字符转换为小写或者大写
    # 11. ljust, rjust：用空格（或者其他字符）填充字符串的空白侧以返回符合最低宽度的字符串
    val = 'a,b, guido'
    show_title("分隔字符串")
    pp(val.split(','))

    pieces = [x.strip() for x in val.split(',')]
    show_title("去除空白符")
    pp(pieces)

    first, second, third = pieces
    show_title("字符串相加")
    pp(first + '::' + second + '::' + third)
    pp('::'.join(pieces))

    show_title("字符串中子串判断")
    show_title("'guido' in val")
    pp('guido' in val)
    show_title("val.index(',')")
    pp(val.index(','))
    show_title("val.index(':')")
    pp(val.index(':'))  # 寻找不存在的字串，会引发异常
    show_title("val.find(':')")
    pp(val.find(':'))
    show_title("val.count(',')")
    pp(val.count(','))
    show_title("val.replace(',','::')")
    pp(val.replace(',', '::'))
    show_title("val.replace(',', '')")
    pp(val.replace(',', ''))


# ch070402. 正则表达式
def ch070402_regular_expressions():
    # Python的re模块的函数可以分为三大类：
    # 1. 模式匹配
    # 2. 替换
    # 3. 拆分
    # P222：表7-4：正则表达式方法
    # 1. findall, finditer：返回字符串中所有的非重叠匹配模式。
    #   - findall：返回的是由所有模式组成的列表
    #   - finditer：返回的是由迭代器逐个返回
    # 2. match：从字符串起始位置匹配模式，还可以对模式各个部分进行分组。
    #   如果匹配到模式，则返回一个匹配项对象，否则返回None
    # 3. search：扫描整个字符串以匹配模式。如果找到则返回一个匹配项对象。
    #   与 match 的不同，其匹配项可以位于字符串的任意位置，不是必须从开始昝匹配
    # 4. split：根据找到的模式将字符串拆分为数段
    # 5. sub, subn：将字符串中所有的（sub）或者前n个（subn）模式替换为指定表达式。
    #   在替换的字符串中可以通过\1、\2等符号表示各个分组项
    import re

    text = "foo bar\t baz \t qux"
    show_title("分隔字符串为单个单词，去除空白符（制表符、空格、换行符等）")
    pp(re.split('\s+', text))

    regex = re.compile('\s+')
    show_title("可征用的regex对象")
    pp(regex.split(text))

    show_title("字符串匹配 regex 模式的所有匹配项")
    pp(regex.findall(text))

    show_title("字符串匹配 regex 模式的第一个匹配项")
    pp(regex.search(text))

    show_title("从字符串开始处匹配 regex 模式")
    pp(regex.match(text))

    text = """
    Dave dave@google.com
    Steve steve@gmail.com
    Rob rob@gmail.com
    Ryan ryan@yahoo.com
    """
    pattern = r'[A-Z0-9._%+-]+@[A-Z0-9-.]+\.[A-Z]{2,4}'
    regex = re.compile(pattern, flags = re.IGNORECASE)
    show_title("寻找文本中的邮件地址")
    pp(regex.findall(text))

    m = regex.search(text)
    show_title("search()返回模式在原字符串中的起始和结束位置")
    pp(m)
    pp(text[m.start():m.end()])
    pp(regex.match(text))

    show_title("sub()将匹配到的模式替换为指定字符串")
    print(regex.sub("邮件地址", text))

    pattern = r'([A-Z0-9._%+-]+)@([A-Z0-0-.]+)\.([A-Z]{2,4})'
    regex = re.compile(pattern, flags = re.IGNORECASE)
    show_title("寻找邮件地址，并且分成3个部分：用户名、域名、域后缀")
    m = regex.match('wesm@bright.net')
    pp(m)
    pp(m.groups())
    show_title("findall()函数返回元组列表")
    pp(regex.findall(text))
    show_title("sub()通过特殊符号访问匹配项中的分组")
    print(regex.sub(r'Username: \1, Domain: \2, Suffix: \3', text))

    regex = re.compile(r"""
    (?P<username>[A-Z0-9._%+-]+)
    @
    (?P<domain>[A-Z0-9-.]+)
    \.
    (?P<suffix>[A-Z]{2,4})""", flags = re.IGNORECASE | re.VERBOSE)
    m = regex.match('wesm@bright.net')
    show_title("带有分组名称的字典")
    print(m.groupdict())


# ch070403. Pandas 中矢量化的字符串函数
def ch070403_vector_str():
    # 即处理矢量化字符串的函数，包括多个字符串变量的存储、搜索、正则表达式处理等等
    # P224，表7-5：矢量化的字符串方法
    # 1. cat：实现元素级的字符串连接操作，可以指定分隔符
    # 2. contains：返回表示各个字符串是否含有指定模式的布尔型数组
    # 3. count：模式的出现次数
    # 4. endswith, startswith：相当于对各个元素执行x.endswith(pattern)或者x.startswith(pattern)
    # 5. findall：计算各个字符串的模式列表
    # 6. get：获取各个元素的第i个字符
    # 7. join：根据指定的分隔符将Series中各个元素的字符串连接起来
    # 8. len：计算各个字符串的长度
    # 9. lower, upper：转换大小写。相当于对各个元素执行x.lower()或者x.upper()
    # 10. match：根据指定的正则表达式对各个元素执行re.match()
    # 11. pad：在字符串的左边、右边或者左右两边添加空白符
    # 12. center：相当于pad(side='both')
    # 13. repeat：重复值。例如：s.str.repeat(3)相当于对各个字符串执行x*3
    # 14. replace：用指定字符串替换找到的模式
    # 15. slice：对Series中的各个字符串进行子串截取
    # 16. split：根据分隔符或者正则表达式对字符串进行拆分
    # 17. strip, rstrip, lstrip：去除空白符，包括：换行符。
    data = {
            'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
            'Rob': 'rob@gmail.com', 'Wes': np.nan
    }
    data = Series(data)
    show_title("原始数据")
    print(data)
    print(data.isnull())
    print(data.str.contains('gmail'))
    pattern = r'([A-Z0-9._%+-]+)@([A-Z0-0-.]+)\.([A-Z]{2,4})'
    regex = re.compile(pattern, flags = re.IGNORECASE)
    print(data.str.findall(pattern, flags = re.IGNORECASE))

    matches = data.str.match(pattern, flags = re.IGNORECASE)
    print(matches)
    print(matches.values)
    print(matches.str.get(1))  # 没有这个功能
    pp(data.str[:5])


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
