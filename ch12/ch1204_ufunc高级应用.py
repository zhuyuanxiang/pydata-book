# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1204_ufunc高级应用.py
@Version    :   v0.1
@Time       :   2019-12-31 16:50
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1204，P383
@Desc       :   NumPy 高级应用，ufunc 高级应用
@理解：主要是些统计工具的应用，对机器学习专业帮助不大
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
# P385，表12-2：ufunc 实例方法
# 1. reduce(x)：连续执行原始运算的方式对值进行聚合
# 2. accumulate(x)：聚合值，保留所有局部聚合结果
# 3. reduceat(x, bins)：“局部”约简（即 groupby）。约简数据的各个切片以产生聚合型数组
# 4. outer(x, y)：对 x 和 y 中的每对元素应用原始运算。结果数组的形状为 x.shape + y.shape
def ch120401_reduce():
    arr = np.arange(10)
    print("np.add.reduce(arr) =", np.add.reduce(arr))
    print("arr.sum() =", arr.sum())

    arr = randn(5, 5)

    show_title("arr")
    pp(arr)
    show_title("arr[::2].sort(1)")
    pp(arr[::2].sort(1))  # 对部分行进行排序
    show_title("arr")
    pp(arr)

    show_title("arr[:, :-1]")
    pp(arr[:, :-1])
    show_title("arr[:, 1:]")
    pp(arr[:, 1:])
    show_title("显示排序的效果")
    show_title("arr[:, :-1] < arr[:, 1:]")
    pp(arr[:, :-1] < arr[:, 1:])

    # logical_and.reduce() 与 all() 等价
    pp(np.logical_and.reduce(arr[:, :-1] < arr[:, 1:], axis = 1))


def ch120402_accumulate():
    # 产生一个与原数组大小相同的中间“累计”值数组
    arr = np.arange(15).reshape((3, 5))
    show_title("arr")
    pp(arr)
    pp(np.add.accumulate(arr, axis = 1))


def ch120403_outer():
    # 计算两个数组的叉积(cross-product)
    arr = np.arange(3).repeat([1, 2, 3])
    show_title("arr")
    pp(arr)
    pp(np.multiply.outer(arr, np.arange(5)))

    pp(np.subtract.outer(np.arange(3), np.arange(3)))
    result = np.subtract.outer(np.arange(12).reshape(3, 4), np.arange(5))
    pp(result)
    print("result.shape =", result.shape)


def ch120404_reduceat():
    # 用于计算“局部约简”，就是一个对数据各个切片进行聚合的 groupby 运算。
    arr = np.arange(10)
    show_title("在 arr[0:5], arr[5:8], arr[8:] 上执行的约简（在本例中是求和）")
    pp(np.add.reduceat(arr, [0, 5, 8]))
    pp(np.subtract.reduceat(arr, [0, 5, 8]))

    arr = np.multiply.outer(np.arange(4), np.arange(5))
    show_title("arr")
    pp(arr)
    pp(np.add.reduceat(arr, [0, 2, 4], axis = 1))


def ch120405_自定义ufunc():
    def add_element(x, y):
        return x + y

    # numpy.frompyfunc() 接受一个 Python 函数和两个分别表示输入输出参数数量的整数
    add_them = np.frompyfunc(add_element, 2, 1)
    pp(add_them(np.arange(8), np.arange(8)))

    # numpy.vectorize() 在类型推断方面更加智能
    add_them = np.vectorize(add_element, otypes = [np.float64])
    pp(add_them(np.arange(8), np.arange(8)))

    # 上面两种自定义 ufunc 型函数的方法比内建的基于 C 的 ufunc 慢


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
