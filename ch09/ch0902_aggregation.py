# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0902_aggregation.py
@Version    :   v0.1
@Time       :   2019-12-26 11:28
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0902，P270
@Desc       :   数据取聚合与分组运算，数据聚合：从数组产生标量值的数据转换过程
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


def peak_to_peak(arr):
    return arr.max() - arr.min()


# ----------------------------------------------------------------------
def ch090200_aggregation():
    # P273，表9-1：经过优化的 groupby 的方法
    # 1. count：分组中非 NA 值的数量
    # 2. sum：分组中非 NA 值的和
    # 3. mean：分组中非 NA 值的平均值
    # 4. median：分组中非 NA 值的算术中位数
    # 5. std, var：无偏的标准差和方差
    # 6. min, max：：分组中非 NA 值的最小值和最大值
    # 7. prod：：分组中非 NA 值的积
    # 8. first, last：分组中非 NA 值的第一个和最后一个
    df = DataFrame({
            'key1': ['a', 'a', 'b', 'b', 'a'],
            'key2': ['one', 'two', 'one', 'two', 'one'],
            'data1': np.random.randn(5), 'data2': np.random.randn(5)
    })
    show_title("原始数据")
    pp(df)

    grouped = df.groupby('key1')
    show_title("计算样本分位数")
    pp(grouped['data1'].quantile(0.9))

    show_title("自定义聚合函数")
    pp(grouped.agg(peak_to_peak))

    show_title("内置统计运算，非聚合运算")
    pp(grouped.describe())


# ch090201. 面向列的多函数应用
def ch090201_multi_function():
    tips = pd.read_csv('../ch08/tips.csv')

    # Add tip percentage of total bill（小费占总额的百分比）
    tips['tip_pct'] = tips['tip'] / tips['total_bill']
    show_title("原始数据")
    pp(tips.head())

    grouped = tips.groupby(['sex', 'smoker'])
    grouped_pct = grouped['tip_pct']
    show_title("以字符串的形式传入的函数")
    pp(grouped_pct.agg('mean'))

    show_title("传入一组函数或者函数名")
    pp(grouped_pct.agg(['mean', 'std', peak_to_peak]))

    show_title("自定义函数对应的列名")
    pp((grouped_pct.agg([('foo', 'mean'), ('bar', np.std)])))

    functions = ['count', 'mean', 'max']
    result = grouped['tip_pct', 'total_bill'].agg(functions)
    show_title("定义一组应用于全部列的函数")
    pp(result)
    pp(result['tip_pct'])
    pp(result['tip_pct']['count'])

    ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
    show_title("自定义名称的元组列表")
    pp(grouped['tip_pct', 'total_bill'].agg(ftuples))

    show_title("定义字典，实现不同的列应用不同的函数")
    pp(grouped.agg({'tip': np.max, 'scale': 'sum'}))

    pp(grouped.agg({'tip_pct': ['min', 'max', 'mean', 'std'], 'scale': 'sum'}))


# ch090202. 以“无索引”的形式返回聚合数据
def ch090202_unindexed():
    tips = pd.read_csv('../ch08/tips.csv')
    show_title("返回的聚合数据中是否含有索引")
    pp(tips.groupby(['sex', 'smoker'], as_index = True).mean())
    pp(tips.groupby(['sex', 'smoker'], as_index = False).mean())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
