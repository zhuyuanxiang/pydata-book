# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0901_groupby.py
@Version    :   v0.1
@Time       :   2019-12-25 12:28
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0901，P263
@Desc       :   数据取聚合与分组运算，GroupBy技术
@理解：分组运算=拆分+应用+合并，图9-1
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


# ----------------------------------------------------------------------
# ch090100. groupby()
def ch090100_groupby():
    df = DataFrame({
            'key1': ['a', 'a', 'b', 'b', 'a'],
            'key2': ['one', 'two', 'one', 'two', 'one'],
            'data1': np.random.randn(5), 'data2': np.random.randn(5)
    })
    show_title("原始数据")
    pp(df)

    grouped = df['data1'].groupby((df['key1']))
    show_title("数据按照 key1 进行分组，计算 data1 列的平均值")
    pp(grouped)
    pp(grouped.mean())

    means = df['data1'].groupby([df['key1'], df['key2']]).mean()
    show_title("数据按照 key1 和 key2 进行分组，计算 data1 列的平均值")
    pp(means)
    pp(means.unstack())

    states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
    years = np.array([2005, 2005, 2006, 2005, 2006])
    my_group_key = np.array([1, 2, 3, 2, 1])
    show_title("分组的键可以是任意长度匹配的数组")
    # 计算用的数据和分组的键可以是相互独立的，不需要放在一个数据结构内
    pp(df['data1'].groupby([states, years]).mean())
    pp(df.groupby(my_group_key).mean())
    pp(df.groupby('key1').mean())
    pp(df.groupby(['key1', 'key2']).mean())
    pp(df.groupby(['key1', 'key2']).size())
    pass


# ch090101. 对分组进行迭代取值
def ch090101_iterate():
    df = DataFrame({
            'key1': ['a', 'a', 'b', 'b', 'a'],
            'key2': ['one', 'two', 'one', 'two', 'one'],
            'data1': np.random.randn(5), 'data2': np.random.randn(5)
    })
    show_title("原始数据")
    pp(df)

    for name, group in df.groupby('key1'):
        # print("name: {}, group: {}".format(name, group))
        print("name: {}".format(name))
        show_title("group")
        print(group)
        pass

    for (k1, k2), group in df.groupby(['key1', 'key2']):
        print("key1: {}, key2: {}".format(k1, k2))
        show_title("group")
        print(group)
        pass

    pieces = dict(list(df.groupby('key1')))
    pp(pieces['b'])
    show_title("数据的类型")
    print(df.dtypes)
    grouped = df.groupby(df.dtypes, axis = 1)
    print(dict(list(grouped)))


# ch090102. 选取一个或者一组列进行分组
def ch090102_select():
    df = DataFrame({
            'key1': ['a', 'a', 'b', 'b', 'a'],
            'key2': ['one', 'two', 'one', 'two', 'one'],
            'data1': np.random.randn(5), 'data2': np.random.randn(5)
    })
    show_title("原始数据")
    pp(df)

    print(df['data1'].groupby(df['key1']))
    # 等价代码
    print(df.groupby('key1')['data1'])

    print(df[['data2']].groupby(df['key2']))
    # 等价代码
    print(df.groupby('key1')[['data2']])

    print(df.groupby(['key1', 'key2'])[['data2']].mean())


# ch090103. 通过字典 或者 Series 进行分组
def ch090103_groupby_dict_series():
    people = DataFrame(np.random.randn(5, 5),
                       columns = ['a', 'b', 'c', 'd', 'e'],
                       index = ['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
    people.ix[2:3, ['b', 'c']] = np.nan
    show_title("原始数据")
    pp(people)

    mapping = {
            'a': 'red', 'b': 'red', 'c': 'blue', 'd': 'blue', 'e': 'red',
            'f': 'orange'
    }
    by_column = people.groupby(mapping)
    by_column = people.groupby(mapping, axis = 1)
    print(by_column.sum())


# ch090104. 通过函数进行分组
def ch090104_groupby_function():
    people = DataFrame(np.random.randn(5, 5),
                       columns = ['a', 'b', 'c', 'd', 'e'],
                       index = ['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
    people.ix[2:3, ['b', 'c']] = np.nan
    show_title("原始数据")
    pp(people)
    show_title("通过函数进行分组")
    print(people.groupby(len).sum())
    show_title("混合函数、数组、列表、字典、Series 进行分组")
    key_list = ['one', 'one', 'one', 'two', 'two']
    print(people.groupby([len, key_list]).min())


# ch090105. 通过索引级别进行分组
def ch090105_groupby_index():
    columns = pd.MultiIndex.from_arrays(
            [['US', 'US', 'US', 'JP', 'JP'], [1, 3, 5, 1, 3]],
            names = ['cty', 'tenor'])
    hier_df = DataFrame(np.random.randn(4, 5), columns = columns)
    show_title("原始数据")
    pp(hier_df)
    print(hier_df.groupby(level = 'cty', axis = 1).count())
    print(hier_df.groupby(level = 'tenor', axis = 1).count())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
