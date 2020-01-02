# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0702_reshape_pivot.py
@Version    :   v0.1
@Time       :   2019-12-22 15:38
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0702，P200
@Desc       :   数据规整化：清理、转换、合并、重塑，重塑和轴向旋转
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import pandas as pd
import winsound
from pandas import DataFrame, Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch070201. 重塑层次化索引
def ch070201_reshape():
    data = DataFrame(np.arange(6).reshape((2, 3)),
                     index = pd.Index(['Ohio', 'Colorado'], name = 'state'),
                     columns = pd.Index(['one', 'two', 'three'],
                                        name = 'number'))
    show_title("原始数据")
    pp(data)

    show_title("stack() 原始数据从列转换为行")
    pp(data.stack())
    show_title("unstack() 原始数据从行转换回列")
    pp(data.unstack())

    result = data.stack()
    show_title("unstack() 从列转换为行的数据从行转换回列，转换最里层")
    pp(result.unstack())

    show_title("stack() 原始数据从列转换为行")
    pp(result)
    show_title("unstack() 从列转换为行的数据从行转换回列，转换最外层")
    pp(result.unstack(0))
    show_title("unstack() 从列转换为行的数据从行转换回列，转换指定层")
    pp(result.unstack('state'))

    s1 = Series([0, 1, 2, 3], index = ['a', 'b', 'c', 'd'])
    s2 = Series([4, 5, 6, ], index = ['c', 'd', 'e'])
    data = pd.concat([s1, s2], keys = ['one', 'two'])
    show_title("原始数据")
    pp(data)
    show_title("unstack() 从列转换为行的数据从行转换回列，缺失数据自动填充")
    pp(data.unstack())
    show_title("stack() 原始数据从列转换为行，缺失数据自动过滤")
    pp(data.unstack().stack())
    show_title("stack() 原始数据从列转换为行，缺失数据禁止过滤")
    pp(data.unstack().stack(dropna = False))

    df = DataFrame({'left': result, 'right': result + 5},
                   columns = pd.Index(['left', 'right'], name = 'side'))
    show_title("原始数据")
    pp(df)
    show_title("DataFrame unstack()")
    pp(df.unstack('state'))
    show_title("DataFrame unstack().stack()")
    pp(df.unstack('state').stack('side'))


# ch070202. 将“长格式”旋转为“宽格式”
def ch070202_pivot():
    data_csv = pd.read_csv('ch07/macrodata.csv')
    periods = pd.PeriodIndex(year = data_csv.year, quarter = data_csv.quarter,
                             name = 'date')
    data = DataFrame(data_csv.to_records(),
                     columns = pd.Index(['realgdp', 'infl', 'unemp'],
                                        name = 'item'),
                     index = periods.to_timestamp('D', 'start'))
    ldata = data.stack().reset_index().rename(columns = {0: 'value'})
    ldata['value2'] = np.random.randn(len(ldata))
    show_title("旋转前的数据")
    pp(ldata.head())
    wdata = ldata.pivot('date', 'item', 'value')
    show_title("旋转后的数据")
    pp(wdata.head())
    wdata = ldata.pivot('date', 'item')
    show_title("不带 value 的旋转后的数据")
    pp(wdata.head())
    unstacked = ldata.set_index(['date', 'item']).unstack('item')
    show_title("pivot 的等价操作")
    pp(unstacked.head())

    show_title("从层次化列中取出指定列的数据")
    pp(wdata['value'].head())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
