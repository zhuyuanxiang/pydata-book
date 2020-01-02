# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1009_性能和内存问题.py
@Version    :   v0.1
@Time       :   2019-12-29 17:27
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1009，P342
@Desc       :   时间序列，性能和内存使用方面需要注意的事项
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
# 越高频率的聚合所需要消耗的时间越长
# ToDo：timeit() 计算速度有问题
rng = pd.date_range('1/1/2000', periods = 10000000, freq = '10ms')
time_series = Series(np.random.randn(len(rng)), index = rng)
print("len(time_series) =", len(time_series))
show_title("time_series")
pp(time_series.head())

show_title("time_series.resample('15min').ohlc()")
pp(time_series.resample('15min').ohlc())

# setup = """
# import pandas as pd
# import numpy as np
# from pandas import DataFrame, Series
# rng = pd.date_range('1/1/2000', periods = 10000000, freq = '10ms')
# time_series = Series(np.random.randn(len(rng)), index = rng)
# """
# print("time_series.resample('15min').ohlc()=", timeit(stmt = "time_series.resample('15min').ohlc()", setup = setup))

rng = pd.date_range('1/1/2000', periods = 10000000, freq = '1s')
time_series = Series(np.random.randn(len(rng)), index = rng)
print("len(time_series) =", len(time_series))
show_title("time_series")
pp(time_series.head())

show_title("time_series.resample('15s').ohlc()")
pp(time_series.resample('15s').ohlc())
# stmt = """
# import pandas as pd
# import numpy as np
# from pandas import DataFrame, Series
# rng = pd.date_range('1/1/2000', periods = 10000000, freq = '1s')
# time_series = Series(np.random.randn(len(rng)), index = rng)
# time_series.resample('15s').ohlc()
# """
# print("time_series.resample('15s').ohlc() =", timeit(stmt))

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
