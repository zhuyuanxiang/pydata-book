# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1203_广播.py
@Version    :   v0.1
@Time       :   2019-12-31 15:38
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1203，P378
@Desc       :   NumPy 高级应用，广播（Broadcasting）：不同形状的数组之间的算术运算方式。
@理解：广播的原则，如果两个数组的后缘维度（Trailing Dimension，即从末尾开始算起的维度）的轴长度相符
或者其中一方的长度为1，则认为它们是广播兼容的。广播会在缺失和（或者）长度为1的维度上进行。
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
arr = np.arange(5)
pp(arr)
pp(arr * 4)  # 标量值4被广播到其他所有的元素上

arr = randn(4, 3)
print("arr.shape =", arr.shape)
show_title("arr")
pp(arr)
print("arr.mean(axis = 0) =", arr.mean(axis = 0))
print("arr.mean(axis = 1) =", arr.mean(axis = 1))
demeaned = arr - arr.mean(0)  # 低维度的数据可以被广播到数组的任意更高维度上
show_title("demeaned")
pp(demeaned)

print("arr.mean(1) =", arr.mean(1))
print("arr.mean(1).shape =", arr.mean(1).shape)
# 根据广播的原则，较小的数组的“广播维”必须为1。
demeaned = arr - arr.mean(1).reshape((4, 1))
show_title("demeaned")
pp(demeaned)
print("demeaned.mean(1) =", demeaned.mean(1))
# 沿其他轴向广播
arr_1d = np.random.normal(size = 3)
show_title("arr_1d[:, np.newaxis]")
arr_2d = arr_1d[:, np.newaxis]
pp(arr_2d)
print("arr_2d.shape =", arr_2d.shape)
show_title("arr_1d[ np.newaxis,:]")
arr_2d = arr_1d[np.newaxis, :]
pp(arr_2d)
print("arr_2d.shape =", arr_2d.shape)

arr = np.zeros((4, 4))
show_title("arr")
pp(arr)
arr_3d = arr[:, np.newaxis, :]
# arr_3d = arr[:, np.newaxis, np.newaxis, :]
print("arr_3d.shape =", arr_3d.shape)
show_title("arr_3d")
pp(arr_3d)

arr = randn(3, 4, 5)
depth_means = arr.mean(2)
show_title("depth_means")
pp(depth_means)
demeaned = arr - depth_means[:, :, np.newaxis]
show_title("demeaned")
pp(demeaned)
print("demeaned.mean(2) =", demeaned.mean(2))


# 对指定的轴进行中心化（距离平均化）
def demean_axis(arr, axis = 0):
    means = arr.mean(axis = axis)
    # 下面这些一般化的东西类似于 N 维的 [:, :, np.newaxis]
    indexer = [slice(None)] * arr.ndim
    indexer[axis] = np.newaxis
    return arr - means(indexer)


# 通过广播设置数组的值
arr = np.zeros((4, 3))
arr[:] = 5
show_title("arr")
pp(arr)

col = np.array([1.28, -0.42, 0.44, 1.6])
arr[:] = col[:, np.newaxis]
show_title("arr")
pp(arr)

arr[:2] = [[-1.37], [0.509]]

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
