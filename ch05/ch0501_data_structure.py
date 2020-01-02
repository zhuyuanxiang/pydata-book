# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0501_data_structure.py
@Version    :   v0.1
@Time       :   2019-12-14 17:14
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0501，P116
@Desc       :   Pandas 入门，Pandas 的数据结构介绍
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
import winsound
from numpy.random import randn
from pandas import DataFrame, Series

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch050101. Series
def ch050101_series():
    obj = Series([4, 7, -5, 3])
    print('-' * 5, "obj", '-' * 5)
    pp(obj)
    print('-' * 5, "obj.values", '-' * 5)
    pp(obj.values)
    print('-' * 5, "obj.index", '-' * 5)
    pp(obj.index)

    obj2 = Series([4, 7, -5, 3], index = ['d', 'b', 'a', 'c'])
    print('-' * 5, "obj2", '-' * 5)
    pp(obj2)
    print('-' * 5, "obj2.index", '-' * 5)
    pp(obj2.index)
    print('-' * 5, "obj2", '-' * 5)
    print("obj2['a'] =", obj2['a'])
    print("obj2['d'] =", obj2['d'])
    print('-' * 5, "obj2[['c', 'a', 'd']]", '-' * 5)
    pp(obj2[['c', 'a', 'd']])

    print('-' * 5, "obj2", '-' * 5)
    pp(obj2)
    print('-' * 5, "obj2[obj2>0]", '-' * 5)
    pp(obj2[obj2 > 0])
    print('-' * 5, "obj2*2", '-' * 5)
    pp(obj2 * 2)
    print('-' * 5, "np.exp(obj2)", '-' * 5)
    pp(np.exp(obj2))

    print('-' * 5, "'b' in obj2", '-' * 5)
    pp('b' in obj2)
    print('-' * 5, "'e' in obj2", '-' * 5)
    pp('e' in obj2)

    sdata = {'北京': 35000, '上海': 71000, '广州': 16000, '成都': 5000}
    print('-' * 5, "使用字典来创建Series", '-' * 5)
    obj3 = Series(sdata)
    print('-' * 5, "obj3", '-' * 5)
    pp(obj3)

    states = ['深圳', '北京', '上海', '广州']
    print('-' * 5, "使用字典来创建 Series，并且指定索引", '-' * 5)
    # Notice: 使用索引创建 Series 带来的不同
    # 1. 不存在的索引名称会被自动赋值为NaN，
    # 2. 不存在于索引的数据会被丢弃，
    # 3. 数据排序会依据索引的顺序，不再按照字典中数据的顺序来排列
    obj4 = Series(sdata, index = states)
    print('-' * 5, "obj4", '-' * 5)
    pp(obj4)

    print('-' * 5, "检查 obj4 数据缺失情况", '-' * 5)
    pp(pd.isnull(obj4))
    pp(pd.notnull(obj4))
    pp(obj4.isnull())
    pp(obj4.notnull())

    print('-' * 5, "obj3 + obj4", '-' * 5)
    pp(obj3 + obj4)

    print("obj4.name =", obj4.name)
    print("obj4.index.name =", obj4.index.name)

    print('-' * 5, "obj", '-' * 5)
    pp(obj)
    obj.index = ['赵二', '张三', '李四', '王五']
    print('-' * 5, "obj", '-' * 5)
    pp(obj)


# ch050102. DataFrame：用关系数据库中表的概念去理解，
# 存储的不是二维数组数据，不能直接取出某行数据，只能根据条件过滤数据，可以直接按列取出数据
def ch050102_DataFrame():
    # Notice: 注意中文显示会错位
    # P123，表5-1：可以输入给 DataFrame 构造器的数据
    # 1. 二维 ndarray ：数据矩阵，还可以传入行标和列标
    # 2. 由数组、列表或者元组组成的字典：每个序列会变成 DataFrame 的一列。所有序列的长度必须相同
    # 3. NumPy 的结构化/记录数组：类似于“由数据组成的字典”
    # 4. 由 Series 组成的字典：每个 Series 会成为一列。如果没有显式指定索引，则各 Series 的索引会被合并成结果的行索引。
    # 5. 由字典组成的字典：各内层字典会成为一列。键会被合并成结果的行索引，跟“由 Series 组成的字典”的情况一样
    # 6. 字典或者 Series 的列表：各项将会成为 DataFrame 的一行。字典键或者 Series 索引的并集将会成为 DataFrame 的列标
    # 7. 由列表或者元组组成的列表：类似于“二维 ndarray”
    # 8. 另一个 DataFrame ：这个 DataFrame 的索引将会被沿用，除非显式指定了其他索引
    # 9. Numpy 的 MaskedArray：类似于“二维 ndarray”的情况，只是 DataFrame 会变成 NA/缺失值

    data = {
            '城市': ['北京', '北京', '北京', '上海', '上海'],
            '年代': [2000, 2001, 2002, 2001, 2002],
            '人口': [1.5, 1.7, 3.6, 2.4, 2.9]
    }
    frame = DataFrame(data)
    print('-' * 5, "生成中文版本的 DataFrame，显示会错列", '-' * 5)
    pp(frame)

    data = {
            'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
    }
    frame = DataFrame(data)
    print('-' * 5, "生成 DataFrame 时,自动添加索引", '-' * 5)
    pp(frame)

    print('-' * 5, "DataFrame 的具体值，数据类型为所有列的数据类型", '-' * 5)
    pp(frame.values)

    frame = DataFrame(data, columns = ['year', 'state', 'pop'])
    print('-' * 5, "frame 指定索引", '-' * 5)
    pp(frame)

    frame2 = DataFrame(data, columns = ['year', 'state', 'pop', 'debt'])
    print('-' * 5, "生成 DataFrame 时,处理缺失列的方式", '-' * 5)
    pp(frame2)

    print('-' * 5, "frame2 取出为 Series 的列", '-' * 5)
    column_state = frame2['state']
    print('-' * 5, "frame2['state']", '-' * 5)
    pp(column_state)
    column_year = frame2.year
    print('-' * 5, "frame2.year", '-' * 5)
    pp(column_year)
    row_three = frame2.loc[4]
    print('-' * 5, "frame2.loc[4]", '-' * 5)
    pp(row_three)

    frame2['debt'] = 16.5
    print('-' * 5, "frame2 缺失列赋值", '-' * 5)
    pp(frame2)

    frame2['debt'] = np.arange(5.)
    print('-' * 5, "frame2 缺失列赋值", '-' * 5)
    pp(frame2)

    val = Series([-1.2, -1.5, -1.7], index = [1, 3, 4])
    frame2['debt'] = val
    print('-' * 5, "frame2 赋值个数不匹配", '-' * 5)
    pp(frame2)

    frame2['eastern'] = frame2.state == 'Ohio'
    print('-' * 5, "frame2 增加新的列", '-' * 5)
    pp(frame2)

    del frame2['eastern']
    print('-' * 5, "frame2 删除列", '-' * 5)
    pp(frame2)

    # 嵌套字典
    pop = {'Nevada': {2001: 2.4, 2002: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
    frame3 = DataFrame(pop)
    print('-' * 5, "使用嵌套字典生成 DataFrame", '-' * 5)
    pp(frame3)

    print('-' * 5, "DataFrame 的转置", '-' * 5)
    pp(frame3.T)

    print('-' * 5, "DataFrame 的具体值", '-' * 5)
    pp(frame3.values)

    frame3.index.name = 'year'
    print('-' * 5, "设置 DataFrame 的索引名称", '-' * 5)
    pp(frame3)

    frame3.columns.name = 'state'
    print('-' * 5, "设置 DataFrame 的列名称", '-' * 5)
    pp(frame3)

    frame4 = DataFrame(pop, index = [2001, 2002, 2003])
    print('-' * 5, "frame4 显式指定索引", '-' * 5)
    pp(frame4)

    pdata = {'Ohio': frame3['Ohio'][:-1], 'Nevada': frame3['Nevada'][:2]}
    frame5 = DataFrame(pdata)
    print('-' * 5, "frame5 使用 Series 生成 frame 的方法 ", '-' * 5)
    pp(frame5)


# ch050103. 索引（index）对象：负责管理轴标签和其他元数据（例如：轴名称等）
def ch050103_index():
    # P125，表5-2：pandas 中主要的 Index 对象
    # 1. Index 类：最泛化的 Index 对象，将轴标签表示为一个由 Python 对象组成的 NumPy 数组
    # 2. Int64Index：针对整数的特殊 Index
    # 3. MultiIndex：“层次化”索引对象，表示单个轴上的多层索引。可以看作由元组组成的数组
    # 4. DatetimeIndex：存储纳秒级时间戳（用 Numpy 的 datetime64 类型表示）
    # 5. PeriodIndex：针对 Period 数据（时间间隔）的特殊 Index
    obj = Series(range(3), index = ['a', 'b', 'c'])
    index = obj.index
    pp(index)
    pp(index[1:])

    # index 对象是不可修改的，因此可以在多个数据结构之间安全共享
    # index[1] = 'd'
    index = pd.Index(np.arange(3))
    obj2 = Series([1.5, -2.5, 0], index = index)

    # P126，表5-3：Index 的方法和属性
    # 1. append：连接另一个 Index 对象，产生一个新的 Index
    # 2. diff：计算差集，并且得到一个 Index
    # 3. intersection：计算交集
    # 4. union：计算并集
    # 5. isin：计算一个指示各值是否都包含在参数集合中的布尔型数组
    # 6. delete：删除索引 i 处的元素，并且得到新的 Index
    # 7. drop：删除传入的值，并且得到新的 Index
    # 8. insert：将元素插入到索引 i 处，并且得到新的 Index
    # 9. is_monotonic：当各个元素均大于等于前一个元素时，返回 True
    # 10. is_unique：当 Index 没有重复值时，返回 True
    # 11. unique：计算 Index 中唯一值的数组

    print("'Ohio' in frame3.columns =", 'Ohio' in frame3.columns)
    print("2001 in frame3.index =", 2001 in frame3.index)
    print("2003 in frame3.index =", 2003 in frame3.index)


# --------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
