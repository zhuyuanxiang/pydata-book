# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0504_missing_data.py
@Version    :   v0.1
@Time       :   2019-12-19 18:41
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0504，P48
@Desc       :   Pandas 入门，处理缺失数据
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from numpy.random import randn
from pandas import DataFrame, Series

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch0504_missing_data():
    string_data = Series(['aardvark', 'artichoke', np.nan, 'avocado'])
    print('-' * 5, "原始数据", '-' * 5)
    pp(string_data)
    print('-' * 5, "非空数据", '-' * 5)
    pp(string_data.isnull())

    string_data[0] = None
    print('-' * 5, "原始数据", '-' * 5)
    pp(string_data)
    print('-' * 5, "非空数据", '-' * 5)
    pp(string_data.isnull())


# ch050401. 滤除缺失数据 dropna()
def ch050401_filter():
    data = Series([1, NA, 3.5, NA, 7])
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "丢弃空数据", '-' * 5)
    pp(data.dropna())
    print('-' * 5, "非空数据掩码矩阵", '-' * 5)
    pp(data.notnull())
    print('-' * 5, "非空数据", '-' * 5)
    pp(data[data.notnull()])

    data = DataFrame([[1., 6.5, 3.], [1., NA, NA], [NA, NA, NA], [NA, 6.5, 3.]])
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "丢弃存在空数据的行", '-' * 5)
    pp(data.dropna())
    print('-' * 5, "丢弃全部是空数据的行", '-' * 5)
    pp(data.dropna(how = 'all'))
    print('-' * 5, "丢弃存在空数据的列", '-' * 5)
    pp(data.dropna(axis = 1))

    data[4] = NA
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "丢弃全部是空数据的列", '-' * 5)
    pp(data.dropna(axis = 1, how = 'all'))

    data = DataFrame(np.random.randn(7, 3))
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    data.loc[:4, 1] = NA
    data.loc[:2, 2] = NA
    print('-' * 5, "切片数据", '-' * 5)
    pp(data)
    print('-' * 5, "thresh 保留至少几个非NA的数据", '-' * 5)
    pp(data.dropna(thresh = 3))


def ch050402_fillna():
    # P152，表5-13：fillna函数的参数
    # 1. value：用于填充缺失值的标量值或者字典对象
    # 2. method：插值方式（ffill，默认，前向填充；bfill，后向填充）
    # 3. axis：待填充的轴，默认=0
    # 4. inplace：替换原始变量的值。默认=False
    # 5. limit：可以连续插值的最大数量，默认=无限制
    data = DataFrame(np.random.randn(7, 3))
    data.loc[:4, 1] = NA
    data.loc[:2, 2] = NA
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "返回填充数据", '-' * 5)
    pp(data.fillna(0))

    data = DataFrame(np.random.randn(7, 3))
    data.loc[:4, 1] = NA
    data.loc[:2, 2] = NA
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "返回填充数据", '-' * 5)
    pp(data.fillna({1: 0.5, 2: -1, 3: 5}))  # 3是没有的列，不填充，不报错

    data = DataFrame(np.random.randn(7, 3))
    data.loc[:4, 1] = NA
    data.loc[:2, 2] = NA
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    data.fillna(0, inplace = True)
    print('-' * 5, "填充原始变量中的数据", '-' * 5)
    pp(data)

    data = DataFrame(np.random.randn(7, 3))
    data.loc[:4, 1] = NA
    data.loc[:2, 2] = NA
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "使用ffill或bfill填充数据", '-' * 5)
    pp(data.fillna(method = 'bfill'))

    data = DataFrame(np.random.randn(7, 3))
    data.loc[:4, 1] = NA
    data.loc[:2, 2] = NA
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "使用ffill或bfill填充数据", '-' * 5)
    pp(data.fillna(method = 'bfill', limit = 2))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
