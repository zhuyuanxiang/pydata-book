# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0505_hierarchical_indexing.py
@Version    :   v0.1
@Time       :   2019-12-20 10:54
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0505，P153
@Desc       :   Pandas 入门，层次化索引
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from pandas import DataFrame, MultiIndex, Series

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch0505. 层次化索引：允许在一个轴上拥有多个（两个以上）的索引级别。
def ch0505_hierarchical_indexing():
    data = Series(np.random.randn(10),
                  index = [['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
                           [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
    print('-' * 5, "多重索引的原始数据", '-' * 5)
    pp(data)
    pp(data.index)
    print('-' * 5, "选取多重索引的子集", '-' * 5)
    pp(data['b'])
    pp(data['b':'c'])
    pp(data.loc[['b', 'd']])
    pp(data[:, 2])
    print('-' * 5, "多重索引的拆开和堆叠，参考ch07", '-' * 5)
    pp(data.unstack())
    pp(data.unstack().stack())

    data = DataFrame(np.arange(12).reshape((4, 3)),
                     index = [['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                     columns = [['Ohio', 'Ohio', 'Colorado'],
                                ['Green', 'Red', 'Green']])
    print('-' * 5, "多重索引和多重列的原始数据", '-' * 5)
    pp(data)
    data.index.names = ['key1', 'key2']
    data.columns.names = ['state', 'color']
    print('-' * 5, "多重索引和多重列的名称", '-' * 5)
    pp(data)
    print('-' * 5, "选取多重列的子集", '-' * 5)
    pp(data['Ohio'])

    index = MultiIndex.from_arrays([['a', 'a', 'b', 'b'], [1, 2, 1, 2]], names = ['key1', 'key2'])
    columns = MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']],
                                     names = ['state', 'color'])
    data = DataFrame(np.arange(12).reshape((4, 3)), index = index, columns = columns)
    print('-' * 5, "使用 MultiIndex 创建的多重索引和多重列的原始数据", '-' * 5)
    pp(data)


# ch050501. 重排分级顺序：重新调整某条轴上各个级别的顺序，或者根据指定级别上的值对数据进行排序
def ch050501_reording_level():
    index = MultiIndex.from_arrays([['a', 'a', 'b', 'b'], [1, 2, 1, 2]], names = ['key1', 'key2'])
    columns = MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']],
                                     names = ['state', 'color'])
    data = DataFrame(np.arange(12).reshape((4, 3)), index = index, columns = columns)
    print('-' * 5, "使用 MultiIndex 创建的多重索引和多重列的原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "调整多重索引关键字的顺序", '-' * 5)
    pp(data.swaplevel('key1', 'key2'))
    print('-' * 5, "删除多重索引某个关键字", '-' * 5)
    pp(data.droplevel('key1'))
    print('-' * 5, "基于某个关键字对索引重新排序", '-' * 5)
    pp(data.sort_index(level = 1))
    pp(data.sort_index(level = 'key2'))
    pp(data.swaplevel(0, 1).sort_index(0))


# ch050502. 根据级别汇总统计
def ch050502_summary_level():
    index = MultiIndex.from_arrays([['a', 'a', 'b', 'b'], [1, 2, 1, 2]], names = ['key1', 'key2'])
    columns = MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']],
                                     names = ['state', 'color'])
    data = DataFrame(np.arange(12).reshape((4, 3)), index = index, columns = columns)
    print('-' * 5, "使用 MultiIndex 创建的多重索引和多重列的原始数据", '-' * 5)
    pp(data)

    print('-' * 5, "根据级别进行汇总", '-' * 5)
    pp(data.sum(level = 'key2'))
    pp(data.sum(level = 'color', axis = 1))


# ch050503. 使用 DataFrame 的列
def ch050503_dataframe_columns():
    data = DataFrame({
            'a': range(7), 'b': range(7, 0, -1),
            'c': ['one', 'one', 'one', 'two', 'two', 'two', 'two'],
            'd': [0, 1, 2, 0, 1, 2, 3]
    })
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "将列转换为索引的数据", '-' * 5)
    pp(data.set_index(['c', 'd']))
    print('-' * 5, "将列转换为索引，但是保留转换列的数据", '-' * 5)
    pp(data.set_index(['c', 'd'], drop = False))
    print('-' * 5, "将索引转换为列的数据", '-' * 5)
    pp(data.set_index(['c', 'd']).reset_index())
    pass


# ----------------------------------------------------------------------
print('-' * 5, "", '-' * 5)
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
