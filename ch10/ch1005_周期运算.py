# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1005_周期运算.py
@Version    :   v0.1
@Time       :   2019-12-28 19:07
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1005，P322
@Desc       :   时间序列，周期的算术运算
@理解
"""
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch100500():
    # Period 类表示时间区间。
    period_1 = pd.Period('2007', freq = 'A-DEC')
    print("period =", period_1)
    print("period + 5 =", period_1 + 5)
    print("period - 2 =", period_1 - 2)
    period_2 = pd.Period('2014', 'A-DEC')
    print("period_2-period_1 =", period_2 - period_1)

    rng = pd.period_range('1/1/2000', '6/30/2000', freq = 'M')
    show_title("rng")
    pp(rng)

    month_series = Series(np.random.randn(6), index = rng)
    show_title("month_series")
    pp(month_series)

    values = ['2001Q3', '2002Q2', '2003Q1']
    index = pd.PeriodIndex(values, freq = 'Q-DEC')
    index = pd.PeriodIndex(values, freq = 'A-DEC')
    index = pd.PeriodIndex(values, freq = 'M')
    index = pd.PeriodIndex(values, freq = 'D')
    pp(index)
    quarter_series = Series(np.random.randn(len(index)), index = index)
    pp(quarter_series)


def ch100501_周期的频率转换():
    # Period 和 PeriodIndex 对象都可以通过 asfreq() 被转换成别的频率
    period = pd.Period('2007', freq = 'A-DEC')
    period = pd.Period('2007', freq = 'A-JAN')
    period = pd.Period('2007', freq = 'A-JUN')
    print("period =", period)
    print("period.asfreq('M', how = 'start') =",
          period.asfreq('M', how = 'start'))
    print("period.asfreq('M', how = 'end') =", period.asfreq('M', how = 'end'))

    period = pd.Period('2007-08', freq = 'M')
    print("period =", period)
    print("period.asfreq('A-JUN') =", period.asfreq('A-JUN'))

    rng = pd.period_range('2006', '2009', freq = 'A-DEC')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    print(time_series)
    show_title("time_series.asfreq('M', how = 'start')")
    print(time_series.asfreq('M', how = 'start'))
    show_title("time_series.asfreq('B', how = 'end')")
    print(time_series.asfreq('B', how = 'end'))


def ch100502_季度周期():
    # Quarter（财年）：Q4表示从11月到1月
    period = pd.Period('2012Q4', freq = 'Q-JAN')
    print("period =", period)
    show_title("period.asfreq('D', 'start')")
    print(period.asfreq('D', 'start'))
    show_title("period.asfreq('D', 'end')")
    print(period.asfreq('D', 'end'))

    p4pm = (period.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
    show_title("获取这个季度倒数第二个工作日下午4点的时间戳")
    print(p4pm)
    print(p4pm.to_timestamp())

    rng = pd.period_range('2011Q3', '2012Q4', freq = 'Q-JAN')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    print(time_series)

    new_rng = (rng.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
    time_series.index = new_rng.to_timestamp()
    show_title("更改 time_series 的索引")
    print(time_series)


def ch100503_Timestamp与Period的转换():
    rng = pd.date_range('1/1/2000', periods = 3, freq = 'M')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    print(time_series)

    pts = time_series.to_period()
    show_title("time_series.to_period()")
    print(pts)

    rng = pd.date_range('1/29/2000', periods = 6, freq = 'D')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    print(time_series)

    pts = time_series.to_period(freq = 'M')
    show_title("time_series.to_period(freq='M')")
    print(pts)

    pts = time_series.to_period()
    show_title("time_series.to_period()")
    print(pts)

    show_title("pts.to_timestamp(how = 'end')")
    print(pts.to_timestamp(how = 'end'))


def ch100504_通过数组创建PeriodIndex():
    data = pd.read_csv('../ch08/macrodata.csv')
    show_title("data.year")
    pp(data.year)
    show_title("data.quarter")
    pp(data.quarter)

    index = pd.PeriodIndex(year = data.year, quarter = data.quarter,
                           freq = 'Q-DEC')
    show_title("index")
    pp(index)

    data.index = index
    pp(data.head())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
