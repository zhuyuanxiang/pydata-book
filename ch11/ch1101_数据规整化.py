# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1101_数据规整化.py
@Version    :   v0.1
@Time       :   2019-12-30 8:21
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec11，P3
@Desc       :   金融和经济数据应用，
@理解
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from numpy.random import randn
from pandas import DataFrame, Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
pd.options.display.max_rows = 12
plt.rc('figure', figsize = (12, 6))


# ----------------------------------------------------------------------
def ch110101_时间序列以及截面对齐():
    close_px = pd.read_csv('ch11/stock_px.csv', parse_dates = True,
                           index_col = 0)
    # prices = close_px.ix['2011-09-05':'2011-09-14', ['AAPL', 'JNJ', 'SPX', 'XOM']]
    prices = close_px.loc['2011-09-05':'2011-09-14',
             ['AAPL', 'JNJ', 'SPX', 'XOM']]
    show_title("prices")
    pp(prices)

    volume_csv = pd.read_csv('ch11/volume.csv', parse_dates = True,
                             index_col = 0)
    # volume = volume_csv.ix['2011-09-05':'2011-09-12', ['AAPL', 'JNJ', 'XOM']]
    volume = volume_csv.loc['2011-09-05':'2011-09-12', ['AAPL', 'JNJ', 'XOM']]
    show_title("volume")
    pp(volume)

    show_title("成交量计算（自动数据对齐）")
    print("prices * volume =")
    pp(prices * volume)

    vwap = (prices * volume).sum() / volume.sum()
    show_title("vwap")
    pp(vwap)
    show_title("vwap.dropna()")
    pp(vwap.dropna())

    show_title("手工对齐，返回一个元组（含有两个对象的重索引版本）")
    pp(prices.align(volume, join = 'inner'))

    series_1 = Series(range(3), index = ['a', 'b', 'c'])
    series_2 = Series(range(4), index = ['d', 'b', 'c', 'e'])
    series_3 = Series(range(3), index = ['f', 'a', 'c'])
    df = DataFrame({'one': series_1, 'two': series_2, 'three': series_3})
    show_title("DataFrame")
    pp(df)

    df = DataFrame({'one': series_1, 'two': series_2, 'three': series_3},
                   index = ['f', 'a', 'c', 'e'])
    df = DataFrame({'one': series_1, 'two': series_2, 'three': series_3},
                   index = list('face'))
    show_title("显式定义结果的索引")
    pp(df)


def ch110102_频率不同的时间序列的运算():
    index = pd.date_range('2012-6-13', periods = 3, freq = 'W-WED')
    time_series_1 = Series(np.random.randn(3), index = index)
    show_title("time_series_1")
    pp(time_series_1)

    show_title("重采样到工作日，出现数据“空洞”")
    resample = time_series_1.resample('B')
    pp(resample.obj)
    pp(list(resample))
    show_title("填充数据“空洞”")
    pp(resample.ffill())

    dates = pd.DatetimeIndex(
            ['2012-6-12', '2012-6-17', '2012-6-18', '2012-6-21', '2012-6-22',
             '2012-6-29', ])
    time_series_2 = Series(np.random.randn(6), index = dates)
    show_title("time_series_2")
    pp(time_series_2)

    show_title("time_series_1+time_series_2")
    pp(time_series_1 + time_series_2)
    show_title("time_series_1 按照 time_series_2 规整")
    pp(time_series_1.reindex(time_series_2.index, method = 'ffill'))
    show_title("time_series_1 按照 time_series_2 规整后 + time_series_2")
    pp(time_series_1.reindex(time_series_2.index,
                             method = 'ffill') + time_series_2)

    # 使用周期（Period）
    gdp_index = pd.period_range('1984Q2', periods = 7, freq = 'Q-SEP')
    gdp = Series([1.78, 1.94, 2.08, 2.01, 2.15, 2.31, 2.46], index = gdp_index)
    show_title("gdp")
    pp(gdp)
    infl_index = pd.period_range('1982', periods = 4, freq = 'A-DEC')
    infl = Series([0.025, 0.045, 0.037, 0.04], index = infl_index)
    show_title("infl")
    pp(infl)

    # 与 Timestamp 的时间序列不同，由 Period 索引的两个不同频率的时间序列之间的运算必须进行显式转换。
    infl_q = infl.asfreq('Q-SEP', how = 'end')
    show_title("infl_q")
    pp(infl_q)

    show_title("可以被重索引的时间序列")
    pp(infl_q.reindex(gdp.index, method = 'ffill'))
    pp(infl_q.reindex(gdp_index, method = 'ffill'))


def ch110103_当天数据和当前数据选择():
    rng = pd.date_range('2012-06-01 09:30', '2012-06-01 15:59', freq = 'T')
    show_title("rng->1个交易日内的日期范围和时间序列")
    pp(rng)

    rng = rng.append([rng + pd.offsets.BDay(i) for i in range(1, 4)])
    show_title("rng->5个交易日内的日期范围和时间序列")
    pp(rng)

    time_series = Series(np.arange(len(rng), dtype = float), index = rng)
    show_title("time_series")
    pp(time_series)

    from datetime import time
    show_title("使用 time 对象进行索引抽取数据")
    pp(time_series[time(10, 0)])
    pp(time_series.at_time(time(10, 0)))
    pp(time_series.between_time(time(10, 0), time(10, 1)))

    # rand_index = np.sort(np.random.permutation(len(time_series))[500:])
    rand_index = np.random.permutation(len(time_series))[700:]
    time_series_rand = time_series.copy()
    time_series_rand[rand_index] = np.nan
    pp(time_series_rand['2012-06-01 09:50':'2012-06-01 10:00'])
    pp(time_series_rand['2012-06-01 09:50':'2012-06-01 10:00'].dropna())

    selection = pd.date_range('2012-06-01 10:00', periods = 4, freq = 'B')
    show_title("使用 Timestamp 的 asof 方法抽取数据")
    pp(time_series_rand.asof(selection))


def ch110104_拼接多个数据源():
    # 目的：在一个特定的时间点上，从一个数据源切换到另一个数据源
    # 方法：使用concat()方法将两个数据源进行拼接
    data1 = DataFrame(np.ones((6, 3), dtype = float), columns = ['a', 'b', 'c'],
                      index = pd.date_range('6/12/2012', periods = 6))
    data2 = DataFrame(np.ones((6, 3), dtype = float) * 2,
                      columns = ['a', 'b', 'c'],
                      index = pd.date_range('6/13/2012', periods = 6))
    spliced = pd.concat([data1.loc[:'2012-06-14'], data2.loc['2012-06-15':]],
                        sort = False)
    show_title("拼接后的数据源")
    pp(spliced)

    data2 = DataFrame(np.ones((6, 4), dtype = float) * 2,
                      columns = ['a', 'b', 'c', 'd'],
                      index = pd.date_range('6/13/2012', periods = 6))
    data3 = DataFrame(np.random.randn(6, 4), columns = ['a', 'b', 'c', 'd'],
                      index = pd.date_range('6/13/2012', periods = 6))
    spliced = pd.concat([data1.loc[:'2012-06-14'], data2.loc['2012-06-15':]],
                        sort = False)
    show_title("拼接列数不同的数据源")
    pp(spliced)

    spliced_filled = spliced.combine_first(data3)
    show_title("使用其他数据源填充不足的数据")
    pp(spliced_filled)

    spliced_copy = spliced.copy()
    spliced_copy.update(data3, overwrite = True)
    show_title("使用其他数据源填充，将原始数据覆盖")
    pp(spliced_copy)
    spliced_copy = spliced.copy()
    spliced_copy.update(data3, overwrite = False)
    show_title("使用其他数据源填充，不将原始数据覆盖")
    pp(spliced_copy)

    spliced_copy = spliced.copy()
    spliced_copy[['a', 'c']] = data1[['a', 'c']]
    show_title("使用其他数据源对应列填充，将原始数据覆盖，注意其他数据源中缺失的数据会将NA填充到目标数据源")
    pp(spliced_copy)


def ch110105_收益指数和收益累计():
    close_px = pd.read_csv('ch11/stock_px.csv', parse_dates = True,
                           index_col = 0)
    # prices = close_px.ix['2011-09-05':'2011-09-14', ['AAPL', 'JNJ', 'SPX', 'XOM']]
    prices = close_px.loc['2011-09-05':'2011-09-14',
             ['AAPL', 'JNJ', 'SPX', 'XOM']]
    show_title("prices")
    pp(prices)
    price = close_px.loc['2011-01-01':'2012-07-27', 'AAPL']
    show_title("两个时间点之间的累计百分比回报")
    pp(price['2011-10-03'] / price['2011-3-1'] - 1)

    returns = price.pct_change()  # 迭代值变化的百分比
    ret_index = (1 + returns).cumprod()
    show_title("收益指数")
    pp(ret_index)
    ret_index[0] = 1
    show_title("收益指数")
    pp(ret_index)

    cum_returns = ret_index.resample('BM', how = 'last').pct_change()
    show_title("指定时期内的累计收益")
    pp(cum_returns['2011'])

    cum_returns = (1 + returns).resample('M', how = 'prod', kind = 'period') - 1
    show_title("重采样聚合从日百分比变化中计算指定时期内的累计收益")
    pp(cum_returns['2011'])

    # ----------------------------------------------------------------------
    # 运行结束的提醒
    winsound.Beep(600, 500)
