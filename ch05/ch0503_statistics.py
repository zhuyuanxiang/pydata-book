# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0503_statistics.py
@Version    :   v0.1
@Time       :   2019-12-19 17:11
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0503，P42
@Desc       :   Pandas 入门，汇总和计算描述统计
@理解：
"""
from datetime import datetime
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import pandas as pd
import winsound
from pandas import DataFrame, Series

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch050300_function():
    df = DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
                   index = ['a', 'b', 'c', 'd'],
                   columns = ['one', 'two'])
    pp(df)
    print('-' * 5, "DataFrame 求和", '-' * 5)
    pp(df.sum())
    print('-' * 5, "DataFrame 求和", '-' * 5)
    pp(df.sum(axis = 1))

    print('-' * 5, "DataFrame 求均值", '-' * 5)
    pp(df.mean(axis = 1, skipna = False))
    pp(df.mean(axis = 1, skipna = True))
    pp(df.idxmin())  # 最小值的索引
    pp(df.idxmax())  # 最大值的索引
    pp(df.cumsum())  # 累加
    pp(df.describe())  # 多个汇总统计

    # 非数值型数据，产生计数统计
    obj = Series(['a', 'a', 'b', 'c'] * 4)
    pp(obj)
    pp(obj.describe())


# ch050301. 相关系数与协方差
def ch050301():
    # 模块已经迁移
    # import pandas.io.data as web
    # for tiker in ['AAPL', 'IBM', 'MSFT', 'GOOG']:
    #     all_data[tiker] = web.get_data_yahoo(tiker, '1/1/2000', '1/1/2010')
    import pandas_datareader.data as web
    all_data = {}
    start = datetime(2010, 1, 1)
    end = datetime(2011, 1, 1)
    for tiker in ['AAPL', 'IBM', 'MSFT', 'GOOG', 'XOM']:
        all_data[tiker] = web.DataReader(tiker, 'yahoo', start, end)

    price = DataFrame({tic: data['Adj Close'] for tic, data in all_data.items()})
    volumn = DataFrame({tic: data['Volume'] for tic, data in all_data.items()})

    returns = price.pct_change()  # 迭代值变化的百分比
    pp(returns.tail())
    pp(returns.MSFT.corr(returns.IBM))  # 相关系数
    pp(returns.MSFT.cov(returns.IBM))  # 协方差
    pp(returns.corr())
    pp(returns.cov())
    pp(returns.corrwith(returns.IBM))
    pp(returns.corrwith(volumn))


# ch050302. 唯一值、值计数以及成员资格
def ch050302():
    obj = Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
    uniques = obj.unique()
    pp(uniques)
    pp(obj.value_counts())
    pp(obj.value_counts(sort = False))
    pp(pd.value_counts(obj.values, sort = False))

    mask = obj.isin(['b', 'c'])
    pp(mask)
    pp(obj[mask])

    data = DataFrame({
            'Qu1': [1, 3, 4, 3, 4],
            'Qu2': [2, 3, 1, 2, 3],
            'Qu3': [1, 5, 2, 4, 4]
    })
    pp(data)
    pp(data.apply(lambda x: x.max()))
    pp(data['Qu1'].value_counts())
    pp(data.apply(pd.value_counts))
    pp(data.apply(pd.value_counts).fillna(0))


print('-' * 5, "", '-' * 5)
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
