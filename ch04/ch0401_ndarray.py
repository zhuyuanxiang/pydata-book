# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0401_ndarray.py
@Version    :   v0.1
@Time       :   2019-12-11 15:45
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0401，P83
@Desc       :   NumPy基础：数组和矢量计算，
@理解：
"""
import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from numpy.random import randn
from pprintpp import pprint as pp

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
data = np.random.randn(2, 3)
print("data =")
pp(data)
print("data * 10 =")
pp(data * 10)
print("data + data =")
pp(data + data)
print("data.shape =", data.shape)
print("data.dtype =", data.dtype)

# 创建 ndarray
# P85，表4-1：数组创建函数
# - array：将输入数据（列表、元组）转换为ndarray，dtype可以靠推断，也可以指定
# - asarray：将输入转换为ndarray
# - arange：功能类似于range，返回的是ndarray
# - ones, ones_like：根据指定形状创建全1数组
# - zeros, zeros_like：根据指定形状创建全0数组
# - empty, empty_like：根据指定形状创建空新数组
# - eye, identity：创建一个全1对角阵
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data1)
pp(arr1)
print("arr1.shape =", arr1.shape)
print("arr1.dtype =", arr1.dtype)
print("arr1.ndim =", arr1.ndim)

data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
pp(arr2)
print("arr2.shape =", arr2.shape)
print("arr2.dtype =", arr2.dtype)
print("arr2.ndim =", arr2.ndim)

data_zeros = np.zeros(10)
pp(data_zeros)
data_zeros = np.zeros((3, 6))
pp(data_zeros)

# np.empty()函数返回的是一些未初始化的垃圾值，不能默认为0
data_empty = np.empty((2, 3, 2))
pp(data_empty)

data_eye = np.eye(3, 4)
pp(data_eye)

data_identity = np.identity(3)
pp(data_identity)

# ndarray 的数据类型
# P86, 表4-2：NumPy 的数据类型
arr1 = np.array([1, 2, 3], dtype = np.float64)
pp(arr1.dtype)

arr2 = np.array([1, 2, 3], dtype = np.int32)
pp(arr2.dtype)

float_arr = arr2.astype(np.float)
pp(float_arr.dtype)

float_arr = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
pp(float_arr)
pp(float_arr.astype(np.int))

numeric_strings = np.array(['1.25', '-9.6', '442'], dtype = np.str)
pp(numeric_strings.astype(float))

int_arr = np.arange(10)
calibers = np.array([.22, .270, .357, .380, .44, .50], dtype = float)
pp(int_arr.astype(calibers.dtype))

empty_unit32 = np.empty(8, dtype = 'u4')
pp(empty_unit32)

# 数组与标量之间的运算
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
pp(arr2 * arr2)
pp(arr2 - np.ones_like(arr2))
pp(1 / arr2)
pp(arr2 ** 0.5)
# 广播（broadcasting）：不同大小数组之间的运算，参考ch12

# 基本的索引和切片
arr = np.arange(10)
pp(arr)
pp(arr[5])
pp(arr[5:8])

arr[5:8] = 12
pp(arr)

# 数组的切片是原始数组的视图
arr_slice = arr[5:8]
arr_slice[1] = 12345
pp(arr)

arr_slice[:] = 64
pp(arr)

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
pp(arr2d[2])
pp(arr2d[0][2] == arr2d[0, 2])

arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
pp(arr3d)
pp(arr3d[0])

old_values = arr3d[0].copy()
arr3d[0] = 42
pp(arr3d)
pp(old_values)
arr3d[0] = old_values
pp(arr3d)
pp(arr3d[1, 0])

# 切片索引
print("arr =", arr)
print("arr[1:6] =", arr[1:6])

print("arr2d =")
pp(arr2d)
print("arr2d[:2] =")
pp(arr2d[:2])
print("arr2d[:2,1:] =")
pp(arr2d[:2, 1:])
print("arr2d[1,:2] =")
pp(arr2d[1, :2])
print("arr2d[:,:1] =")
pp(arr2d[:, :1])

print("arr2d =")
pp(arr2d)
arr2d[:2, 1:] = 0
print("arr2d =")
pp(arr2d)

# 布尔型索引
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
print("names =")
pp(names)

data = randn(7, 4)
data = np.arange(28).reshape((7, 4))  # reshape() 的使用参考ch12
print("data =")
pp(data)

pp(names == 'Bob')
pp(names != 'Bob')
pp(data[names == 'Bob'])
pp(data[~(names == 'Bob')])
pp(data[names == 'Bob', 2:])
pp(data[names == 'Bob', 3])

mask = (names == 'Bob') | (names == 'Will')
pp(mask)
pp(data[mask])

# ToKnown: Python 的关键字 and 和 or 在布尔型数组中无效
data[data < 10] = 0
pp(data)

data[names != 'Joe'] = 7
pp(data)

# 花式索引(Fancy indexing)：利用整数数组进行索引
arr = np.empty((8, 4))
for i in range(8):
    arr[i] = i
    pass
pp(arr)
print("arr[[4,3,0,6]] =")
pp(arr[[4, 3, 0, 6]])
print("arr[[-3,-5,-7]] =")
pp(arr[[-3, -5, -7]])

arr = np.arange(32).reshape((8, 4))
pp(arr)
pp(arr[[1, 5, 7, 2]])
# pp(arr[[1, 5, 7, 2], [0, 1, 2]])  # 形状必须匹配
pp(arr[[1, 5, 7, 2], [0, 3, 1, 2]])
pp(arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])  # 这个才是期望的矩阵
pp(arr[np.ix_([1, 5, 7, 2], [0, 3, 1, 2])])
pp(arr[np.ix_([1, 5, 7, 2], [0, 3, 1])])

# 数组转置和轴对称
arr = np.arange(15).reshape((3, 5))
pp(arr)
pp(arr.T)

arr = randn(6, 3)
np.dot(arr.T, arr)

# 高维数据变换，可以先将每个值的下标标出，然后对下标进行转换就可以理解了。
arr = np.arange(16).reshape((2, 2, 4))
pp(arr)
pp(arr.transpose())
pp(arr.transpose((0, 1, 2)))
pp(arr.transpose((1, 0, 2)))
# pp(arr.transpose((0, 1))) # 必须一次变换所有轴
pp(arr.swapaxes(0, 1))  # 可以选择交换两个轴
pp(arr.swapaxes(1, 2))
pp(arr.swapaxes(0, 2))

arr = np.arange(4).reshape((2, 2, 1))
pp(arr)
pp(arr.T)

arr = np.arange(4).reshape((2, 2))
pp(arr)
pp(arr.T)

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
