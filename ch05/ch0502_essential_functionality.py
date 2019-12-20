# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0502_essential_functionality.py
@Version    :   v0.1
@Time       :   2019-12-19 11:17
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0502，P126
@Desc       :   Pandas 入门，基本功能
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from pandas import DataFrame, Series

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch050201. 重新索引
def ch050201():
    obj = Series([4.5, 7.2, -5.3, 3.6], index = ['d', 'b', 'a', 'c'])
    print('-' * 5, "初步的顺序", '-' * 5)
    pp(obj)

    obj2 = obj.reindex(['a', 'b', 'c', 'd', 'e'])
    print('-' * 5, "重排的顺序，不存在的索引值使用缺失值", '-' * 5)
    pp(obj2)

    obj3 = obj.reindex(['a', 'b', 'c', 'd', 'e'], fill_value = 0)
    print('-' * 5, "重排的顺序，不存在的索引值使用设置的默认值", '-' * 5)
    pp(obj3)

    obj4 = Series(['blue', 'purple', 'yellow'], index = [0, 2, 4])
    print('-' * 5, "初步的顺序", '-' * 5)
    pp(obj4)

    # P127，表5-4：reindex的（插值）method选项
    # 1. ffill或者pad：前向填充（或者搬运）值
    # 2. bfill或者backfill：后向填充（或者搬运）值
    # P129，表5-5：reindex 函数的参数
    # 1. index：用作索引的新序列。即可以是Index实例，也可以是其他序列型的Python数据结构。Index会被完全使用，就像没有任何复制一样
    # 2. method：插值（填充）方式，具体参数参考表5-4
    # 3. fill_value：在重新索引的过程中，需要引入缺失值时使用的替代值
    # 4. limit：前向或者后向填充时的最大填充量
    # 5. level：在MultiIndex的指定级别上匹配简单索引，否则选取其子集
    # 6. copy：默认为True，无论如何都复制；如果为False，则新旧相等就不复制
    obj5 = obj4.reindex(range(6), method = 'ffill')
    print('-' * 5, "重排的顺序，不存在的索引值使用前向值", '-' * 5)
    pp(obj5)

    frame = DataFrame(np.arange(9).reshape((3, 3)), index = ['a', 'c', 'd'], columns = ['Ohio', 'Texas', 'California'])
    print('-' * 5, "生成 DataFrame，设置索引和列", '-' * 5)
    pp(frame)

    frame2 = frame.reindex(['a', 'b', 'c', 'd'])
    print('-' * 5, "重新索引行，插入新的行，使用缺失值", '-' * 5)
    pp(frame2)

    states = ['Texas', 'Utah', 'California']
    frame3 = frame.reindex(columns = states)
    print('-' * 5, "使用 columns 关键字即可重新索引列，新增的列使用缺失值", '-' * 5)
    pp(frame3)

    # frame4 = frame.reindex(method = 'ffill', columns = states)    # 这两个方法不可以一起操作
    frame4 = frame.reindex(index = ['a', 'b', 'c', 'd'], columns = states)
    frame4 = frame.reindex(index = ['a', 'b', 'c', 'd'], method = 'ffill')
    print('-' * 5, "", '-' * 5)
    pp(frame4)

    # 不允许使用下面这个办法
    # print('-' * 5, "ix方法已经被放弃了", '-' * 5)
    # frame.ix[['a', 'b', 'c', 'd'], states]


# ch050202. 丢弃指定轴上的项
def ch050202():
    obj = Series(np.arange(5.), index = ['a', 'b', 'c', 'd', 'e'])
    print('-' * 5, "原始数据", '-' * 5)
    pp(obj)
    new_obj = obj.drop('c')
    print('-' * 5, "丢弃某个索引的数据", '-' * 5)
    pp(new_obj)

    data = DataFrame(np.arange(16.).reshape(4, 4),
                     index = ['Ohio', 'Colorado', 'Utah', 'New York'],
                     columns = ['one', 'two', 'three', 'four'])
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "丢弃某个索引的数据", '-' * 5)
    pp(data.drop(['Colorado', 'Ohio']))
    print('-' * 5, "丢弃某个列的数据", '-' * 5)
    pp(data.drop('two', axis = 1))
    pp(data.drop(['two', 'four'], axis = 1))


# ch050203. 索引、选取和过滤：
def ch050203():
    obj = Series(np.arange(4.), index = ['a', 'b', 'c', 'd'])
    pp(obj)
    print('-' * 5, "取一个数据", '-' * 5)
    pp(obj[1])
    pp(obj['b'])
    print('-' * 5, "取连续数据", '-' * 5)
    pp(obj[2:4])
    pp(obj['b':'c'])
    print('-' * 5, "取多个数据", '-' * 5)
    pp(obj[['b', 'a', 'd']])
    print('-' * 5, "根据值取数据", '-' * 5)
    pp(obj[[1, 3]])
    print('-' * 5, "根据条件取数据", '-' * 5)
    pp(obj[obj < 2])

    obj['b':'c'] = 5
    print('-' * 5, "修改数据", '-' * 5)
    pp(obj)

    data = DataFrame(np.arange(16.).reshape(4, 4),
                     index = ['Ohio', 'Colorado', 'Utah', 'New York'],
                     columns = ['one', 'two', 'three', 'four'])
    print('-' * 5, "原始数据", '-' * 5)
    pp(data)
    print('-' * 5, "取一个数据", '-' * 5)
    pp(data['two'])
    print('-' * 5, "取多个数据", '-' * 5)
    pp(data[['three', 'one']])
    print('-' * 5, "取连续数据", '-' * 5)
    pp(data[:2])
    print('-' * 5, "根据条件取数据", '-' * 5)
    pp(data[data['three'] > 5])

    print('-' * 5, "掩码矩阵", '-' * 5)
    pp(data > 5)

    data[data < 5] = 0
    print('-' * 5, "修改数据", '-' * 5)
    pp(data)

    # print('-' * 5, "ix方法已经被放弃了", '-' * 5)
    # pp(data.ix['Colorado', ['two', 'three']])
    # pp(data.ix[['Colorado', 'Utah'], [3, 0, 1]])
    # pp(data.ix[2])
    # pp(data.ix[:'Utah', 'two'])
    # pp(data.ix[data.three > 5, :3])


# ch050204. 算术运算和数据对齐：对不同索引的对象进行算术运算
def ch050204():
    s1 = Series([7.3, -2.5, 3.4, 1.5], index = ['a', 'c', 'd', 'e'])
    s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index = ['a', 'c', 'e', 'f', 'g'])
    pp(s1)
    pp(s2)
    pp(s1 + s2)

    df1 = DataFrame(np.arange(9.).reshape((3, 3)), columns = list('bcd'), index = ['Ohio', 'Texas', 'Colorado'])
    df2 = DataFrame(np.arange(12.).reshape((4, 3)), columns = list('bde'), index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
    pp(df1)
    pp(df2)
    pp(df1 + df2)


# ch050205. 在算术方法中填充值
def ch050205():
    s1 = Series([7.3, -2.5, 3.4, 1.5], index = ['a', 'c', 'd', 'e'])
    s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index = ['a', 'c', 'e', 'f', 'g'])
    pp(s1)
    pp(s2)
    df1 = DataFrame(np.arange(9.).reshape((3, 3)), columns = list('bcd'), index = ['Ohio', 'Texas', 'Colorado'])
    df2 = DataFrame(np.arange(12.).reshape((4, 3)), columns = list('bde'), index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
    pp(df1)
    pp(df2)

    pp(df1.add(df2, fill_value = 0))


# ch050206. DataFrame 和 Series 之间的运算
def ch050206():
    s1 = Series([7.3, -2.5, 3.4, 1.5], index = ['a', 'c', 'd', 'e'])
    s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index = ['a', 'c', 'e', 'f', 'g'])
    pp(s1)
    pp(s2)
    df1 = DataFrame(np.arange(9.).reshape((3, 3)), columns = list('bcd'), index = ['Ohio', 'Texas', 'Colorado'])
    df2 = DataFrame(np.arange(12.).reshape((4, 3)), columns = list('bde'), index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
    pp(df1)
    pp(df2)

    # 支持的操作
    pp(s1 + df1)
    pp(df1.add(s1))
    pp(s1 - df1)
    pp(df1.sub(s1))

    # 不支持的操作
    # pp(s1.add(df1))

    pp(df1.sub(df1['d'], axis = 0))


# ch050207. 函数应用和映射
def ch050207():
    frame = DataFrame(np.random.randn(4, 3), columns = list('bde'), index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
    pp(frame)
    pp(np.abs(frame))

    f = lambda x: x.max() - x.min()
    print('-' * 5, "将函数应用到由各列或者各行所形成的一维数组", '-' * 5)
    pp(frame.apply(f))
    pp(frame.apply(f, axis = 1))

    def f(x):
        return Series([x.min(), x.max()], index = ['min', 'max'])

    print('-' * 5, "将函数应用到由各列或者各行所形成的一维数组", '-' * 5)
    pp(frame.apply(f))
    pp(frame.apply(f, axis = 1))

    format = lambda x: '%.2f' % x
    format = lambda x: '{:.2f}'.format(x)
    print('-' * 5, "将格式化函数应用到由各列或者各行所形成的一维数组", '-' * 5)
    pp(frame.applymap(format))


# ch050208. 排序和排名
def ch050208_sort():
    obj = Series(range(4), index = ['d', 'a', 'b', 'c'])
    print('-' * 5, "原始的 Series", '-' * 5)
    pp(obj)
    print('-' * 5, "排序后的 Series", '-' * 5)
    pp(obj.sort_index())  # 对索引排序
    pp(obj.sort_values())  # 对值排序

    frame = DataFrame(np.arange(8).reshape((2, 4)), index = ['three', 'one'], columns = ['d', 'a', 'b', 'c'])
    print('-' * 5, "原始的 DataFrame", '-' * 5)
    pp(frame)
    print('-' * 5, "排序后的 DataFrame", '-' * 5)
    pp(frame.sort_index())
    pp(frame.sort_index(axis = 0))
    pp(frame.sort_index(axis = 1))
    pp(frame.sort_index(axis = 1, ascending = False))
    pp(frame.reindex(columns = ['a', 'b', 'c', 'd']).sort_index())
    pp(frame.sort_values('a'))

    obj = Series([4, 7, -3, 2])
    pp(obj)
    pp(obj.sort_values())  # order()函数已经被sort_values()取代

    obj = Series([4, np.nan, 7, np.nan, -3, 2])
    pp(obj)
    pp(obj.sort_values())

    frame = DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})
    pp(frame)
    pp(frame.sort_index(by = 'b'))
    pp(frame.sort_values(by = 'b'))
    pp(frame.sort_values(by = ['a', 'b']))


def ch050208_rank():
    # rank()相对于sort 函数，给出的是值在序列中的位置，但是整个序列的顺序没有改变
    # P141，表5-8：排名时用于破坏平级关系的 method 选项
    # 1. average：（默认），在相等分组中，为各个值分配平均排名
    # 2. min：使用整个分组的最小排名
    # 3. max：使用整个分组的最大排名
    # 4. first：按值在原始数据中的出现顺序分配排名
    obj = Series([7, -5, 7, 4, 2, 0, 4])
    pp(obj.sort_index())
    pp(obj.rank(method = 'first'))
    pp(obj.rank())
    pp(obj.rank(method = 'average'))
    pp(obj.rank(ascending = False, method = 'max'))

    frame = DataFrame({'b': [4.3, 7, -3, 2], 'a': [0, 1, 0, 1], 'c': [-2, 5, 8, -2.5]})
    pp(frame)
    pp(frame.rank(axis = 0))
    pp(frame.rank(axis = 1))


# ch050209. 带有重复值的轴索引
def ch050209():
    obj = Series(range(5), index = ['a', 'a', 'b', 'b', 'c'])
    pp(obj)
    pp(obj['a'])
    pp(obj['c'])
    pp(obj.index.is_unique)

    df = DataFrame(np.random.randn(4, 3), index = ['a', 'a', 'b', 'b'])
    pp(df)
    pp(df.ix['b'])
    pp(df.loc['b'])
    pp(df.iloc[2:4])


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
