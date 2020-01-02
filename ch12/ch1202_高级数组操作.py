# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1202_高级数组操作.py
@Version    :   v0.1
@Time       :   2019-12-30 17:24
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1202，P370
@Desc       :   NumPy 高级应用，高级数组操作
@理解
"""
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import winsound

from tools import show_title

# 设置数据显示的精确度为小数点后4位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch120201_数组重塑():
    arr = np.arange(8)
    print("arr =", arr)
    show_title("arr.reshape((4,2))")
    pp(arr.reshape((4, 2)))
    show_title("arr.reshape((4,2)).reshape((2,4))")
    pp(arr.reshape((4, 2)).reshape((2, 4)))

    arr = np.arange(15)
    show_title("arr.reshape((5,-1))")
    pp(arr.reshape((5, -1)))

    other_arr = np.ones((3, 5))
    print("other_arr.shape =", other_arr.shape)
    show_title("arr.reshape(other_arr.shape)")
    pp(arr.reshape(other_arr.shape))

    arr = np.arange(15).reshape((5, 3))
    show_title("arr")
    pp(arr)

    arr_flatten = arr.flatten()  # flatten() 会对“源数据”产生副本
    print("arr.flatten() =", arr_flatten)
    arr_flatten[10] = 9
    show_title("修改了 arr_flatten 后，arr 不变")
    pp(arr)

    arr_ravel = arr.ravel()  # ravel() 不会对“源数据”产生副本
    print("arr.ravel() =", arr_ravel)
    arr_ravel[10] = 12
    show_title("修改了 arr_ravel 后，arr 改变")
    pp(arr)


def ch120202_C的顺序和Fortran的顺序():
    arr = np.arange(12).reshape((3, 4))
    show_title("arr")
    pp(arr)
    print("arr.ravel() =", arr.ravel())  # 默认（C)
    print("arr.ravel() =", arr.ravel('C'))  # C（C语言）：行优先顺序。
    print("arr.ravel() =", arr.ravel('F'))  # F（Fortran）：列优先顺序
    print("arr.ravel() =", arr.ravel('A'))  # A 与 K 用的较少
    print("arr.ravel() =", arr.ravel('K'))


def ch120203_数组的合并与拆分():
    # 数组的合并，P374，表12-1：数组连接函数
    # 1. concatenate：沿一条轴连接一组数组
    # 2. vstack, row_stack：以面向行的方式对数组进行堆叠（沿轴0）
    # 3. hstack：以面向列的方式对数组进行堆叠（沿轴1）
    # 4. column_stack：类似于hstack，需要先将一维数组转换为二维列向量
    # 5. dstack：以面向“深度”的方式对数组进行堆叠
    arr_1 = np.array([1, 2, 3, 4, 5, 6])
    arr_2 = np.array([7, 8, 9, 10, 11, 12])

    arr_stack(arr_1, arr_2)

    arr_1 = np.array([[1, 2, 3], [4, 5, 6]])
    arr_2 = np.array([[7, 8, 9], [10, 11, 12]])

    arr_stack(arr_1, arr_2)

    arr_1 = np.array([[[1], [2], [3]], [[4], [5], [6]]])
    arr_2 = np.array([[[7], [8], [9]], [[10], [11], [12]]])

    arr_stack(arr_1, arr_2)

    arr_1 = np.array([[[1, 2, 3], [4, 5, 6]]])
    arr_2 = np.array([[[7, 8, 9], [10, 11, 12]]])

    arr_stack(arr_1, arr_2)

    arr_1 = np.array([[[[1, 2, 3], [4, 5, 6]]]])
    arr_2 = np.array([[[[7, 8, 9], [10, 11, 12]]]])

    arr_stack(arr_1, arr_2)

    # 数组的拆分，P374，表12-1：数组拆分函数
    # 1. split：沿指定轴在指定的位置拆分数组
    # 2. hsplit, vsplit, dsplit：沿轴0，轴1，轴2 进行拆分
    arr = np.random.randn(11, 2)
    show_title("arr")
    pp(arr)

    first, second, third, forth = np.split(arr, indices_or_sections = [1, 5,
                                                                       10])  # 切分的位置
    show_title("first")
    pp(first)
    show_title("second")
    pp(second)
    show_title("third")
    pp(third)
    show_title("forth")
    pp(forth)

    # 堆叠辅助类：r_ 和 c_
    arr = np.arange(6)
    arr_1 = arr.reshape((3, 2))
    arr_2 = np.random.randn(3, 2)
    show_title("np.r_ 行堆叠")
    pp(np.r_[arr_1, arr_2])
    show_title("np.c_ 列堆叠")
    pp(np.c_[arr_1, arr_2])
    show_title("将切片翻译成数组")
    pp(np.c_[1:6, -10:-5])


def arr_stack(arr_1, arr_2):
    show_title("np.concatenate([arr1,arr2],axis=0)")
    pp(np.concatenate([arr_1, arr_2], axis = 0))
    show_title("np.vstack((arr_1, arr_2))")
    pp(np.vstack((arr_1, arr_2)))
    show_title("np.hstack((arr_1, arr_2))")
    pp(np.hstack((arr_1, arr_2)))
    show_title("np.column_stack((arr_1, arr_2))")
    pp(np.column_stack((arr_1, arr_2)))
    show_title("np.dstack((arr_1, arr_2))")
    pp(np.dstack((arr_1, arr_2)))


def ch120204_元素的重复操作():
    # repeat()：没指定轴向重复数组中的元素一定次数
    arr = np.arange(3)
    print("arr.repeat(3) =", arr.repeat(3))
    print("arr.repeat([2, 3, 4]) =", arr.repeat([2, 3, 4]))
    print("arr.repeat([2, 3, 4, 5]) =", arr.repeat([2, 3, 4, 5]))  # 形状不匹配，结果报错

    arr = np.random.randn(2, 2)
    show_title("二维数组")
    pp(arr)

    show_title("arr.repeat(2, axis = 0)")
    pp(arr.repeat(2, axis = 0))
    show_title("arr.repeat(2, axis =1)")
    pp(arr.repeat(2, axis = 1))

    show_title("arr.repeat([2, 3], axis = 0)")
    pp(arr.repeat([2, 3], axis = 0))
    show_title("arr.repeat([2, 3], axis =1)")
    pp(arr.repeat([2, 3], axis = 1))

    # tile()：沿指定轴向堆叠数组的副本
    # tile() 与 repeat() 的区别：（重复区域的大小）
    # 1. repeat() 对单个元素进行重复
    # 2. tile() 对整块数组进行重复
    arr = np.random.randn(2, 2)
    show_title("二维数组")
    pp(arr)

    show_title("np.tile(arr, 2)")
    pp(np.tile(arr, 2))

    show_title("np.tile(arr,(2,))")
    pp(np.tile(arr, (2,)))

    show_title("np.tile(arr,(2,1))")
    pp(np.tile(arr, (2, 1)))

    show_title("np.tile(arr,(3,2))")
    pp(np.tile(arr, reps = (3, 2)))

    arr = np.random.randn(2, 2, 1)
    show_title("三维数组")
    pp(arr)

    show_title("np.tile(arr, 2)")
    pp(np.tile(arr, 2))

    show_title("np.tile(arr,(2,))")
    pp(np.tile(arr, (2,)))

    show_title("np.tile(arr,(2,1))")
    pp(np.tile(arr, (2, 1)))

    show_title("np.tile(arr,(3,2))")
    pp(np.tile(arr, reps = (3, 2)))

    show_title("np.tile(arr,(3,2,2))")
    pp(np.tile(arr, reps = (3, 2, 2)))  # reps表示沿着哪个轴向重复几次


def ch120205_花式索引():
    # 获取和设置数组子集：通过整数数组使用花式索引
    arr = np.arange(10) * 10
    inds = [7, 1, 2, 6]
    print("arr[inds] =", arr[inds])

    # take() & put()
    print("arr.take(inds) =", arr.take(inds))

    print("arr =", arr)
    arr.put(inds, 42)
    print("arr.put() 后的 arr =", arr)
    arr.put(inds, [40, 41, 42, 43])
    print("arr.put() 后的 arr =", arr)

    arr = np.random.rand(3, 4)
    inds = [2, 1, 0, 1, 2]
    show_title("arr")
    pp(arr)
    show_title("在指定轴上使用 take()")
    show_title("arr.take(inds, axis = 0)")
    pp(arr.take(inds, axis = 0))
    show_title("arr.take(inds, axis = 1)")
    pp(arr.take(inds, axis = 1))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
