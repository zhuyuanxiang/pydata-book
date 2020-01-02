# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1006_重采样及频率转换.py
@Version    :   v0.1
@Time       :   2019-12-28 19:56
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1006，P327
@Desc       :   时间序列，重采样及频率转换
@理解：重采样（resampling)指的是将时间序列从一个频率转换到另一个频率的处理过程。
降采样（downsampling)指的是将高频率数据聚合到低频率数据。
升采样（Upsampling）指的是将低频率数据转换到高频率数据。
"""
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
def ch100600_resample():
    # P328，表10-5：resample 方法的参数
    # 1. freq：重采样的频率。可以使用字符串｛'M', '5min'｝或者 DateOffset｛Second(15)｝定义
    # 2. how：用于产生聚合值的函数名称或者数组函数。默认（mean），包括：first, last, median, mean, ohlc, max, min
    # 已经废弃，直接在后面调用相应的聚合函数
    # 3. axis：重采样的轴。默认（0）
    # 4. fill_method：升采样时如何插值。默认（None，不插值），包括：ffill, bfill
    # 已经废弃，直接在后面调用相应的填充函数
    # 4.1. limit=None：在前向或者后向填充时，允许填充的最大时期数
    # 已经移入到填充函数中。
    # 5. closed='right'：在降采样中，各个时间段的哪一段是闭合（即包含）的。默认（right)，包括：left, right
    # 6. label='right'：在降采样中，如何设置聚合值的标签，箱子的边界。默认（right）
    # 例如：9:30到9:35之间的这5分钟会被标记为9:30或者9:35。right 就会标记为9:35。
    # 7. loffset=None：箱子标签的时间校正值，例如：'-1s'或者 Second(-1)用于将聚合标签调早1秒
    # 9. kind=None：聚合到时期（'period'）或者 时间戳（'timestamp'）。默认聚合到时间序列的索引类型。
    # 10. convention=None：当重采样周期时，将低频率转换到高频率决定将各个区间的哪个端用于放置原来的值。
    # 默认（'end'），包括：start, end
    rng = pd.date_range('1/1/2000', periods = 100, freq = 'D')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    pp(time_series)
    pp(time_series.resample('M', how = 'mean'))
    pp(time_series.resample('M').mean())
    pp(time_series.resample('M', kind = 'period').mean())


def ch100601_降采样():
    # 降采样需要关注的点：
    # 1. 各个区间的闭合
    # 2. 如何标记各个聚合的箱子，用区间的开头还是末尾
    rng = pd.date_range('1/1/2000', periods = 12, freq = 'T')
    time_series = Series(np.arange(len(rng)), index = rng)
    show_title("time_series")
    pp(time_series)
    pp(time_series.resample('5min').sum())
    pp(time_series.resample('5min', loffset = '-1s').sum())
    pp(time_series.resample('5min', closed = 'right').sum())
    pp(time_series.resample('5min', closed = 'left').sum())
    pp(time_series.resample('5min', closed = 'left', label = 'right').sum())
    pp(time_series.resample('5min', closed = 'left', label = 'left').sum())

    # OHLC 重采样
    # 金融领域中的时间序列聚合方式：
    # 1. 开盘（Open）
    # 2. 收盘（Close）
    # 3. 最大值（High）
    # 4. 最小值（Low）
    pp(time_series.resample('5min').ohlc())

    # 通过 groupby 进行重采样
    rng = pd.date_range('1/1/2000', periods = 100, freq = 'D')
    time_series = Series(np.random.randn(len(rng)), index = rng)
    show_title("time_series")
    pp(time_series)
    show_title("对月份进行分组")
    pp(time_series.groupby(lambda x: x.month).mean())
    show_title("对星期几进行分组")
    pp(time_series.groupby(lambda x: x.weekday).mean())


def ch100602_升采样和插值():
    df = DataFrame(np.random.randn(2, 4),
                   index = pd.date_range('1/1/2000', periods = 2,
                                         freq = 'W-WED'),
                   columns = ['Colorado', 'Texas', 'New York', 'Ohio'])
    show_title("原始数据")
    pp(df)

    df_daily = df.resample('D')
    pp(list(df_daily))
    pp(df.resample('D', fill_method = 'ffill'))
    pp(df.resample('D').ffill())
    show_title("与原始数据中的日期索引不相交")
    pp(df.resample('W-THU').ffill())
    pp(df.resample('D').ffill(limit = 2))


def ch100603_根据周期进行重采样():
    # 在降采样中，目标频率必须是源频率的子周期（subperiod）
    # 在升采样中，目标频率必须是源频率的超周期（superperiod）
    df = DataFrame(np.random.randn(24, 4),
                   index = pd.period_range('1-2000', '12-2001', freq = 'M'),
                   columns = ['Colorado', 'Texas', 'New York', 'Ohio'])
    show_title("原始数据")
    pp(df)

    annual_df = df.resample('A-DEC').mean()
    show_title("annual_df")
    pp(annual_df)

    show_title("按季度填充")
    pp(annual_df.resample('Q-MAR').ffill())
    # Q-DEC：季度型（每年以12月结束）
    show_title("按季度填充")
    pp(annual_df.resample('Q-DEC').ffill())
    show_title("按季度填充，默认（convention = 'start'）")
    pp(annual_df.resample('Q-DEC', convention = 'start').ffill())
    show_title("按季度填充，（convention = 'end'）")
    pp(annual_df.resample('Q-DEC', convention = 'end').ffill())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
