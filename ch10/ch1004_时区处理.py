# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1004_时区处理.py
@Version    :   v0.1
@Time       :   2019-12-28 17:00
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1004，P317
@Desc       :   时间序列，时区处理
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
# daylight savings time (DST，夏令时)
# coordinated universal time (UTC，协调世界时）：代替Greenwich Mean Time（GMC，格林威治时间），国际标准
import pytz

show_title("pytz.common_timezones[-5:]")
pp(pytz.common_timezones[-5:])

tz = pytz.timezone('US/Eastern')
show_title("pytz.timezone('US/Eastern')")
pp(tz)


def ch100401_本地化():
    rng = pd.date_range('3/9/2012 9:30', periods = 6, freq = 'D', tz = 'UTC')
    show_title("rng")
    print(rng)

    rng = pd.date_range('3/9/2012 9:30', periods = 6, freq = 'D')
    show_title("rng")
    print(rng)
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    pp(time_series)
    time_series_utc = time_series.tz_localize('UTC')
    show_title("time_series_utc")
    pp(time_series_utc)
    show_title("time_series_utc.tz_convert('US/Eastern')")
    pp(time_series_utc.tz_convert('US/Eastern'))

    show_title("index.tz")
    print("time_series.index.tz =", time_series.index.tz)
    print("time_series_utc.index.tz =", time_series_utc.index.tz)

    time_series_eastern = time_series.tz_localize('US/Eastern')
    show_title("time_series_eastern")
    pp(time_series_eastern)
    show_title("time_series_eastern.tz_convert('UTC')")
    pp(time_series_eastern.tz_convert('UTC'))
    show_title("time_series_eastern.tz_convert('Europe/Berlin')")
    pp(time_series_eastern.tz_convert('Europe/Berlin'))

    print("time_series.index.tz_localize('Asia/Shanghai') =")
    pp(time_series.index.tz_localize('Asia/Shanghai'))


def ch100402_操作Timestamp对象():
    stamp = pd.Timestamp('2011-03-12 04:00')
    stamp_utc = stamp.tz_localize('utc')
    print("stamp_utc.tz_convert('US/Eastern') =")
    pp(stamp_utc.tz_convert('US/Eastern'))

    stamp_moscow = pd.Timestamp('2011-03-12 04:00', tz = 'Europe/Moscow')
    print("stamp_moscow =", stamp_moscow)
    print("stamp_utc.value =", stamp_utc.value)
    print("stamp_utc.tz_convert('US/Eastern').value =",
          stamp_utc.tz_convert('US/Eastern').value)

    from pandas.tseries.offsets import Hour

    # 夏令时转变前30分钟
    stamp = pd.Timestamp('2012-03-12 01:30', tz = 'US/Eastern')
    print("stamp =", stamp)
    print("stamp+Hour() =", stamp + Hour())

    # 夏令时转变前90分钟
    stamp = pd.Timestamp('2012-11-04 00:30', tz = 'US/Eastern')
    print("stamp =", stamp)
    print("stamp + 2 * Hour() =", stamp + 2 * Hour())  # 注意这个时间变化


def ch100403_不同时区():
    rng = pd.date_range('3/9/2012 9:30', periods = 6, freq = 'B')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    pp(time_series)

    time_series_1 = time_series[:7].tz_localize('Europe/London')
    time_series_2 = time_series_1[2:].tz_convert('Europe/Moscow')
    result = time_series_1 + time_series_2
    show_title("result.index")
    pp(result.index)


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
