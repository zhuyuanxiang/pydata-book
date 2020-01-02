# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0506_others.py
@Version    :   v0.1
@Time       :   2019-12-20 13:44
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0506，P158
@Desc       :   Pandas 入门，其他有关 Pandas 的话题
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from numpy.random import randn
from pandas import Series

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch050601. 整数索引
def ch050601_integer_indexing():
    data = Series(np.arange(3.))
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    data[-1]  # 会报错的代码，因为带来参数混淆（-1是“标签”，还是“位置”）

    data = Series(np.arange(3.), index = ['a', 'b', 'c'])
    pp(data[-1])  # 不会报错的代码，-1是“位置”
    pp(data[:1])
    pp(data.ix[:1])

    data = Series(range(3), index = [-5, 1, 3])
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    pp(data.iloc[2])
    pp(data.iat[2])


# ch050602. 面板数据结构：三维的DataFrame。已经在 1.0 的版本中被移除
def ch050602_Panel():
    pass


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
