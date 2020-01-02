# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1002_时间序列基础.py
@Version    :   v0.1
@Time       :   2019-12-28 12:40
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1002，P307
@Desc       :   时间序列，时间序列基础
@理解
"""
from datetime import datetime
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame, Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch100200_时间序列():
    dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
             datetime(2011, 1, 8), datetime(2011, 1, 10),
             datetime(2011, 1, 12), ]
    time_series = Series(np.random.randn(6), index = dates)
    show_title("time_series")
    pp(time_series)
    print("type(time_series) =", end = '')
    print(type(time_series))

    show_title("index")
    pp(time_series.index)
    show_title("time_series[::2]")
    pp(time_series[::2])
    show_title("time_series + time_series[::2]")
    pp(time_series + time_series[::2])

    stamp = time_series.index[0]
    print("time_series.index[0] =", end = '')
    pp(stamp)


def ch100201_索引():
    dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
             datetime(2011, 1, 8), datetime(2011, 1, 10),
             datetime(2011, 1, 12), ]
    time_series = Series(np.random.randn(6), index = dates)
    show_title("time_series")
    pp(time_series)
    stamp = time_series.index[2]
    print("time_series[stamp] =", time_series[stamp])
    print("time_series['1/07/2011'] =", time_series['1/07/2011'])
    print("time_series['20110107'] =", time_series['20110107'])

    longer_ts = Series(np.random.randn(1000),
                       index = pd.date_range('1/1/2000', periods = 1000))
    show_title("longer_ts")
    pp(longer_ts.head())
    show_title("longer_ts['2001'] =")
    print(longer_ts['2001'].head())
    show_title("longer_ts['2001-05'] =")
    print(longer_ts['2001-05'].head())
    show_title("longer_ts['2001-05-01':'2001-05-02'] =")
    print(longer_ts['2001-05-01':'2001-05-02'].head())
    show_title("longer_ts[datetime(2001,5,1)] =")
    print(longer_ts[datetime(2001, 5, 1)])
    show_title("截断长的时间序列数据")
    print(longer_ts.truncate(after = '5/1/2001'))

    show_title("对 DataFrame 进行索引")
    dates = pd.date_range('1/1/2000', periods = 100, freq = 'W-WED')
    long_df = DataFrame(np.random.randn(100, 4), index = dates,
                        columns = ['Colorado', 'Texas', 'New York', 'Ohio'])
    print(long_df.loc['5-2001'])


def ch100202_重复索引的时间序列():
    dates = pd.DatetimeIndex(
            ['1/1/2000', '1/2/2000', '1/2/2000', '1/2/2000', '1/3/2000'])
    dup_ts = Series(np.arange(5), index = dates)
    show_title("dup_ts")
    print(dup_ts)
    show_title("检查索引是否重复")
    print("dup_ts.index.is_unique =", dup_ts.index.is_unique)
    print("dup_ts['1/3/2000'] =", dup_ts['1/3/2000'])
    print("dup_ts['1/2/2000'] =")
    pp(dup_ts['1/2/2000'])

    show_title("数据聚合")
    grouped = dup_ts.groupby(level = 0)
    print(grouped.mean())
    print(grouped.count())
    print(grouped.describe())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
