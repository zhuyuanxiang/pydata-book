# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0701_merging_datasets.py
@Version    :   v0.1
@Time       :   2019-12-21 17:35
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0701，P186
@Desc       :   数据规整化：清理、转换、合并、重塑，
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
# 合并数据集的方法：
# 1. pandas.merge：根据一个或者多个键将不同的DataFrame中的行连接起来。类似于关系数据库的连接操作。
# 2. pandas.concat：沿着一个轴将多个对象堆叠在一起
# 3. self.combine_first：将重复数据编连在一起，用一个对象中的值填充另一个对象中的缺失值。

# ch070101. 数据库风格的 DataFrame 合并
def ch070101_merge_dataframe():
    # P190，表7-1：merge函数的参数
    # 1. left：参与合并的左侧DataFrame
    # 2. right：参与合并的右侧DataFrame
    # 3. how：merge 的连接方式：inner（默认）、left、right、outer[参考关系数据库]
    # 4. on：用于连接的列名。必须存在于左右两个DataFrame对象中。
    # 如果没有指定就使用两个对象的列名交集作为连接键。
    # 如果没有相同名字的列名，即连接键集合为空，就会报错。
    # 5. left_on：左侧DataFrame中作为连接键的列
    # 6. right_on：右侧DataFrame中作为连接键的列
    # 7. left_index：左侧的行索引作为连接键
    # 8. right_index：右侧的行索引作为连接键
    # 9. sort：根据连接键对合并后的数据进行排序。默认（True）。
    # 对于大数据集，建议设为（False），提高连接性能。
    # 10. suffixes：字符串值元组，用于追加到重叠列名的末尾，默认（'_x','_y'）。
    # 11. copy：是否复制新的数据。默认（True）
    data1 = DataFrame(
            {'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': range(7)})
    data2 = DataFrame({'key': ['a', 'b', 'd'], 'data2': range(3)})
    show_title("data1")
    pp(data1)
    show_title("data2")
    pp(data2)
    show_title("data1 使用 inner（默认） 连接 data2")
    pp(pd.merge(data1, data2))
    show_title("显式指定关键字")
    pp(pd.merge(data1, data2, on = 'key'))
    show_title("data1 使用 left 连接 data2")
    pp(pd.merge(data1, data2, how = 'left'))
    show_title("data1 使用 right 连接 data2")
    pp(pd.merge(data1, data2, how = 'right'))
    show_title("data1 使用 outer 连接 data2")
    pp(pd.merge(data1, data2, how = 'outer'))

    show_title("data2 使用 inner（默认） 连接 data1")
    pp(pd.merge(data2, data1))
    show_title("data1 merge data2 sort by data2")
    pp(pd.merge(data1, data2).sort_values(by = 'data2'))
    show_title("data2 merge data1 sort by data1")
    pp(pd.merge(data2, data1).sort_values(by = 'data1'))

    data3 = DataFrame(
            {'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': range(7)})
    data4 = DataFrame({'rkey': ['a', 'b', 'd'], 'data2': range(3)})
    show_title("第一个数据集的关键字指定 和 第二个数据集的关键字指定")
    pp(pd.merge(data3, data4, left_on = 'lkey', right_on = 'rkey'))

    left = DataFrame({
            'key1': ['foo', 'foo', 'bar'], 'key2': ['one', 'two', 'one'],
            'lval': [1, 2, 3]
    })
    right = DataFrame({
            'key1': ['foo', 'foo', 'bar', 'bar'],
            'key2': ['one', 'one', 'one', 'two'], 'rval': [4, 5, 6, 7]
    })
    pp(pd.merge(left, right, on = ['key1', 'key2'], how = 'outer'))

    pp(pd.merge(left, right, on = 'key1'))

    pp(pd.merge(left, right, on = 'key1', suffixes = ('_left', '_right')))
    pass


# ch070102. 索引上的合并
def ch070102_merge_index():
    left = DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'], 'value': range(6)})
    show_title("left")
    pp(left)
    right = DataFrame({'group_val': [3.5, 7]}, index = ['a', 'b'])
    show_title("right")
    pp(right)
    show_title("left1的连接键为key，right1的连接键为index，inner为交集，outer为并集")
    pp(pd.merge(left, right, left_on = 'key', right_index = True))
    pp(pd.merge(left, right, left_on = 'key', right_index = True,
                how = 'outer'))

    left = DataFrame({
            'key1': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
            'key2': [2000, 2001, 2002, 2001, 2002], 'data': np.arange(5.)
    })
    show_title("left")
    pp(left)
    right = DataFrame(np.arange(12).reshape((6, 2)), index = [
            ['Nevada', 'Nevada', 'Ohio', 'Ohio', 'Ohio', 'Ohio'],
            [2001, 2000, 2000, 2000, 2001, 2002]],
                      columns = ['event1', 'event2'])
    show_title("right")
    pp(right)
    show_title("层次化索引数据连接")
    pp(pd.merge(left, right, left_on = ['key1', 'key2'], right_index = True))
    pp(pd.merge(left, right, left_on = ['key1', 'key2'], right_index = True,
                how = 'outer'))
    # 列中数据不匹配时会报错
    # pp(pd.merge(left, right, left_on = ['key2', 'key1'], right_index = True))

    left = DataFrame([[1., 2.], [3., 4.], [5., 6.]], index = ['a', 'c', 'e'],
                     columns = ['Ohio', 'Nevada'])
    show_title("left")
    pp(left)
    right = DataFrame([[7., 8.], [9., 10.], [11., 12.], [13., 14.]],
                      index = ['b', 'c', 'd', 'e'],
                      columns = ['Missouri', 'Alabama'])
    show_title("right")
    pp(right)
    show_title("左右侧都使用索引作为连接键")
    pp(pd.merge(left, right, left_index = True, right_index = True))

    show_title("使用 join 进行按索引合并")
    pp(left.join(right, how = 'inner'))
    pp(left.join(right))  # join() 的参数 how 默认为 left
    pp(left.join(right, how = 'left'))
    pp(left.join(right, how = 'outer'))

    left = DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'], 'value': range(6)})
    show_title("left")
    pp(left)
    right = DataFrame({'group_val': [3.5, 7]}, index = ['a', 'b'])
    show_title("right")
    pp(right)
    show_title("指定 join 的连接键")
    pp(left.join(right, on = 'key'))

    left = DataFrame([[1., 2.], [3., 4.], [5., 6.]], index = ['a', 'c', 'e'],
                     columns = ['Ohio', 'Nevada'])
    show_title("left")
    pp(left)
    right = DataFrame([[7., 8.], [9., 10.], [11., 12.], [13., 14.]],
                      index = ['b', 'c', 'd', 'e'],
                      columns = ['Missouri', 'Alabama'])
    show_title("right")
    pp(right)
    another = DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]],
                        index = ['a', 'c', 'e', 'f'],
                        columns = ['New York', 'Oregon'])
    show_title("another")
    pp(another)
    show_title("索引合并，也可以看作数据堆叠")
    pp(left.join([right, another]))
    pp(left.join([right, another], how = 'outer'))


# ch070103. 轴向连接（contatenation)，也叫绑定（binding）或者堆叠(stacking）
def ch070103_concat():
    # numpy 的 contatenate
    arr = np.arange(12).reshape((3, 4))
    show_title("原始数据")
    pp(arr)
    show_title("沿第一个轴堆叠")
    pp(np.concatenate([arr, arr]))
    show_title("沿第二个轴堆叠")
    pp(np.concatenate([arr, arr], axis = 1))

    # pandas 的 contat
    # P198，表7-2：concat 函数的参数
    # 1. objs：参与连接的 pandas 对象的列表或者字典。唯一必需的参数
    # 2. axis：指明连接的轴向。默认（0）
    # 3. join：指明其他轴向上的索引是按交集（inner）还是并集（outer）进行合并。默认（outer）
    # 4. join_axes：指明用于其他 n-1 条轴的索引，不执行并集/交集运算
    # 5. keys：与连接对象有关的值，用于形成连接轴向上的层次化索引。
    # 可以是任意值的列表或者数组、元组数组、数组列表（需要将 levels 设置成多级数组）
    # 6. levels：指定作为层次化索引各个级别上的索引（需要设置 keys）
    # 7. names：作为创建分层级别的名称。（需要设置 keys 和/或 levels）
    # 8. verify_integrity：检查结果对象新轴上的重复情况，重复则引发异常。默认（False），即允许重复。
    # 9. ignore_index：产生一组新的索引range(total_length)替换连接轴上的索引，
    s1 = Series([0, 1, 2], index = ['a', 'b', 'c'])
    s2 = Series([2, 3, 4, ], index = ['c', 'd', 'e'])
    s3 = Series([5, 6], index = ['f', 'g'])
    show_title("沿第一个轴堆叠")
    pp(pd.concat([s1, s2, s3]))
    show_title("沿第二个轴堆叠")
    pp(pd.concat([s1, s2, s3], axis = 1))

    s4 = pd.concat([s1 * 5, s3])
    show_title("s4")
    pp(s4)
    show_title("s1 & s4 沿第二个轴堆叠")
    pp(pd.concat([s1, s4], axis = 1))
    show_title("指定连接方式")
    pp(pd.concat([s1, s4], axis = 1, join = 'inner'))
    show_title("指定索引")
    pp(pd.concat([s1, s4], axis = 1, join_axes = [['a', 'c', 'b', 'e']]))
    show_title("创建层次化索引")
    pp(pd.concat([s1, s1, s3], keys = ['one', 'two', 'three']))

    df1 = DataFrame(np.arange(6).reshape((3, 2)), index = ['a', 'b', 'c'],
                    columns = ['one', 'two'])
    show_title("df1")
    pp(df1)

    df2 = DataFrame(5 + np.arange(4).reshape((2, 2)), index = ['a', 'c'],
                    columns = ['three', 'four'])
    show_title("df2")
    pp(df2)

    show_title("DataFrame concat")
    pp(pd.concat([df1, df2], axis = 1, keys = ['level1', 'level2'],
                 sort = True))
    pp(pd.concat([df1, df2], axis = 1, keys = ['level1', 'level2'],
                 ignore_index = True, sort = True))
    pp(pd.concat([df1, df2], axis = 1, keys = ['level1', 'level2'],
                 names = ['upper', 'lower'], sort = True))
    pp(pd.concat({'level1': df1, 'level2': df2}, axis = 1, sort = True))


# ch070104. 合并堆叠数据
def ch070104_combining_data_with_overlap():
    s1 = Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
                index = ['f', 'e', 'd', 'c', 'b', 'a'])
    s2 = Series(np.arange(len(s1), dtype = np.float64),
                index = ['f', 'e', 'd', 'c', 'b', 'a'])
    s2[-1] = np.nan
    show_title("使用 s2 中的数据替换 s1 中的空数据")
    pp(np.where(pd.isnull(s1), s2, s1))

    show_title("pandas 中 Series 的 combine_first()")
    pp(s1.combine_first(s2))
    pp(s1[:-2].combine_first(s2[2:]))
    pp(s2[:-2].combine_first(s1[2:]))

    df1 = DataFrame({
            'a': [1., np.nan, 5., np.nan], 'b': [np.nan, 2., np.nan, 6.],
            'c': range(2, 18, 4)
    })
    df2 = DataFrame({
            'a': [5., 4., np.nan, 3., 7.], 'b': [np.nan, 3., 4., 6., 8.]
    })

    show_title("pandas 中 DataFrame 的 combine_first()")
    pp(df1.combine_first(df2))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
