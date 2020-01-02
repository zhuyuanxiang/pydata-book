# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1206_排序.py
@Version    :   v0.1
@Time       :   2020-01-01 11:20
@License    :   (C)Copyright 2018-2020, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1206，P388
@Desc       :   NumPy 高级应用，排序
@理解
"""
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import winsound
from numpy.random import randn

from tools import show_title

# 设置数据显示的精确度为小数点后4位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch120600_sort():
    arr = randn(6)
    show_title("arr")
    pp(arr)
    show_title("arr.sort()")
    arr.sort()
    pp(arr)

    arr = randn(3, 5)
    show_title("arr")
    pp(arr)
    show_title("arr[:, 0].sort()")
    arr[:, 0].sort()  # 对第一个列排序
    pp(arr)
    show_title("arr[:, 0:2].sort()")
    arr[:, 0:2].sort()  # 默认对行排序
    pp(arr)
    show_title("arr.sort()")
    arr.sort()  # 默认对行排序
    pp(arr)
    show_title("arr.sort(axis = 1)")
    arr.sort(axis = 1)  # 默认对行排序
    pp(arr)
    show_title("arr反序的技巧 = arr[:, ::-1]")
    pp(arr[:, ::-1])

    arr = randn(5)
    show_title("arr")
    pp(arr)
    show_title("np.sort(arr)")
    pp(np.sort(arr))  # 对原始数据建立排序后的副本
    pp(arr)


def ch120601_间接排序_argsort():
    values = np.array([5, 0, 1, 3, 2])
    indexer = values.argsort()
    show_title("排序后的索引。indexer")
    pp(indexer)
    show_title("排序后的值。values[indexer]")
    pp(values[indexer])

    arr = randn(3, 5)
    arr[0] = values
    show_title("arr")
    pp(arr)
    show_title("利用第一行的索引数据对整个数组排序")
    pp(arr[:, arr[0].argsort()])


def ch120601_间接排序_lexsort():
    # lexsort() 可以一次性对多个键数组执行间接排序（字典序）
    first_name = np.array(['Bob', 'Jane', 'Steve', 'Bill', 'Barbara'])
    last_name = np.array(['Jones', 'Arnold', 'Arnold', 'Jones', 'Walters'])
    sorter = np.lexsort((first_name, last_name))
    pp(list(zip(last_name[sorter], first_name[sorter])))


def ch120602_其他排序算法():
    values = np.array(['2:first', '2:second', '1:first', '1:second', '1:third'])
    key = np.array([2, 2, 1, 1, 1])
    indexer = key.argsort(kind = 'mergesort')  # mergesort（合并排序）是稳定排序。
    show_title("indexer")
    pp(indexer)
    show_title("values.take(indexer)")
    pp(values.take(indexer))


def ch120603_searchsorted():
    # searchsorted()：在有序数组上执行二分查找的数组方法，只要将值插入到它返回的那个位置就能维持数组的有序性
    arr = np.array([0, 1, 7, 12, 15])
    print(("arr.searchsorted(9) =", arr.searchsorted(9)))
    print("arr.searchsorted([0, 8, 11, 16]) =",
          arr.searchsorted([0, 8, 11, 16]))

    arr = np.array([0, 0, 0, 1, 1, 1, 1])
    print("arr.searchsorted([0, 1]) =", arr.searchsorted([0, 1]))
    print("arr.searchsorted([0, 1], side = 'right') =",
          arr.searchsorted([0, 1], side = 'right'))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
