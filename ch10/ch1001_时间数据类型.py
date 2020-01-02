# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1001_时间数据类型.py
@Version    :   v0.1
@Time       :   2019-12-28 10:37
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1001，P303
@Desc       :   时间序列，时间数据类型
@理解：本章的内容需要较多的金融知识会容易理解。
"""
from datetime import datetime, timedelta
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from dateutil.parser import parse

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch100101_datetime():
    # P304，表10-1：datetime 模块中的数据类型
    # 1. date：以公历形式存储日历日期（年、月、日）
    # 2. time：将时间存储为时、分、秒、毫秒
    # 3. datetime：存储日期和时间
    # 4. timedelta：表示两个 datetime 值之间的差（日、秒、毫秒）
    now = datetime.now()
    pp(now)
    pp(datetime(2019, 12, 28, 10, 40, 52, 679334))
    print(now.year, now.month, now.day)

    delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
    print("delta =", delta)
    pp(delta)
    print("delta.days =", delta.days)
    print("delta.seconds =", delta.seconds)

    start = datetime(2011, 1, 7)
    print("start =")
    pp(start)
    print("start + timedelta(12) =")
    pp(start + timedelta(12))
    print("start - timedelta(12) =")
    pp(start - timedelta(12))
    print("start - 2 * timedelta(12) =")
    pp(start - 2 * timedelta(12))


def ch100102_字符串转换():
    # P305，表10-2：datetime 格式定义（兼容 ISO C89）
    # 1. %Y：4位数的年
    # 2. %y：2位数的年
    # 3. %m：2位数的月[01,12]
    # 4. %d：2位数的日[01,31]
    # 5. %H：时（24小时制）[00,23]
    # 6. %l：时（12小时制）[01,12]
    # 7. %M：2位数的分[00,59]
    # 8. %S：秒[00,61]（秒60和61用于闰秒）
    # 9. %w：用整数表示的星期几[0（星期天）,6]
    # 10. %U：每年的第几周[00,53]。星期天是每周的第一天，每年的第一个星期天之前的那几天被认为是“第0周”
    # 11. %W：每年的第几周[00,53]。星期一是每周的第一天，每年的第一个星期一之前的那几天被认为是“第0周”
    # 12. %z：以+HHMM或者-HHMM表示的UTC时区偏移量，如果时区为 naive，则返回空字符串
    # 13. %F：%Y-%m-%d的简写形式
    # 14. %D：%m/%d/%y的简写形式
    show_title("str <-> datetime")
    stamp = datetime(2011, 1, 3)
    print("str(stamp) =")
    pp(str(stamp))
    print("stamp.strftime('%Y-%m-%d') =")
    pp(stamp.strftime('%Y-%m-%d'))

    value = '2011-01-03'
    print("value =", value)
    print("datetime.strptime(value, '%Y-%m-%d') =")
    pp(datetime.strptime(value, '%Y-%m-%d'))

    show_title("parse()")
    print("parse('2011-01-03') =")
    pp(parse('2011-01-03'))
    print("parse('Jan 31, 1997 10:45 PM') =")
    pp(parse('Jan 31, 1997 10:45 PM'))
    print("parse('6/12/2011', dayfirst = True) =")
    pp(parse('6/12/2011', dayfirst = True))

    show_title("date strings")
    datestrs = ['7/6/2011', '8/6/2011']
    print("datestrs =")
    pp(datestrs)
    print("[datetime.strptime(x, '%m/%d/%Y') for x in datestrs] =")
    pp([datetime.strptime(x, '%m/%d/%Y') for x in datestrs])
    print("pd.to_datetime(datestrs) =")
    pp(pd.to_datetime(datestrs))

    show_title("idx")
    idx = pd.to_datetime(datestrs + [None])
    print("idx = pd.to_datetime(datestrs + [None] =")
    pp(idx)
    print("idx[2] =")
    pp(idx[2])  # NaT(Not a Time)
    print("pd.isnull(idx) =")
    pp(pd.isnull(idx))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
