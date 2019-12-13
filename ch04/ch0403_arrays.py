# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0403_arrays.py
@Version    :   v0.1
@Time       :   2019-12-12 10:20
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0403，P100
@Desc       :   NumPy基础：数组和矢量计算，利用数组进行数据处理
@理解：将许多数据处理任务表述为简洁的数组表达式，避免了使用循环来处理。
写惯了SQL的同学可以感觉到使用NumPy就如在使用SQL处理数据库里的数据
"""
import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from numpy.random import randn

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
# ch040301.矢量化：用数组表达式代替循环。广播也是矢量化计算方法。（ch12）
# 准备数据
x = np.arange(-2, 2, 1)
y = np.arange(-1, 1, 1)
# 将两个一维数组配对成两个二维矩阵
# 将两个数组中的元素建立一一映射的关系元组(x,y)，再把元组(x,y)拆成两个数组
# 理解：将第一个数组按行重复，重复次数为第二个数组的长度；将第二个数组按列重复，重复次数为第一个数组的长度
xs, ys = np.meshgrid(x, y)
# 1. 计算函数sqrt(x^2 + y^2)
z = np.sqrt(xs ** 2 + ys ** 2)
print("x =")
print(x)
print("xs =")
print(xs)
print("xs ** 2 =")
print(xs ** 2)
print("y =")
print(y)
print("ys =")
print(ys)
print("ys ** 2 =")
print(ys ** 2)
print("(xs^2+ys^2) =")
print(xs ** 2 + ys ** 2)
print("z = sqrt(xs^2+ys^2) =")
print(z)

# 更高级的案例
points = np.arange(-5, 5, 0.01)  # 1000个间隔相等的点
xs, ys = np.meshgrid(points, points)
z = np.sqrt(xs ** 2 + ys ** 2)

plt.imshow(z, cmap = plt.cm.gray)
plt.colorbar()
plt.title("图4-3：根据网格对函数$\sqrt{x^2+y^2}$求值的结果")

# ch040302.将条件逻辑表述为数组运算
xarr = np.arange(1.1, 1.6, 0.1)
yarr = np.arange(2.1, 2.6, 0.1)
cond = np.array([True, False, True, True, False])
print("xarr =", xarr)
print("yarr =", yarr)
print("cond =", cond)
# 使用列表推导式按条件取数
result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
print("result =", result)
# 存在的问题：
# 1. 对大数组的处理速度较慢
# 2. 无法应用于多维数组
# 3. 还会出现多余的尾巴
# 解决办法：np.where(condition, x=None, y=None)
result = np.where(cond, xarr, yarr)
print("result =", result)

# 将数组中大于0的数标为2，否则标为-2
arr = randn(4, 4)
print("np.where(arr > 0, 2, -2) =")
print(np.where(arr > 0, 2, -2))
print("np.where(arr > 0, 2, arr) =")
print(np.where(arr > 0, 2, arr))

cond1, cond2 = np.array([True, True, False, False]), np.array([True, False, True, False])
# np.where()的嵌套
np.where(cond1 & cond2, 0,
         np.where(cond1, 1,
                  np.where(cond2, 2, 3)))
# 等价于
result = []
for i in range(len(cond1)):
    if cond1[i] and cond2[i]:
        result.append(0)
    elif cond1[i]:
        result.append(1)
    elif cond2[i]:
        result.append(2)
    else:
        result.append(3)
        pass
    pass
print("result =", result)

# 数学函数和统计方法
# P104，表4-5：基本数组统计方法（聚合aggregation计算，也叫约简reduction）
# sum：对数组中全部或者某个轴向的元素求和。零长度的数组为0
# mean：对数组中全部或者某个轴向的元素求均值。零长度的数组为NaN
# std, var：对数组中全部或者某个轴向的元素求方差和标准差。零长度的数组为NaN
# min, max：对数组中全部或者某个轴向的元素求最小值和最大值。零长度的数组报错
# argmin, argmax：对数组中全部或者某个轴向的元素求最小值的索引和最大值的索引。零长度的数组报错
# cumsum：对数组中全部或者某个轴向的元素求累计和。零长度的数组返回零长度数组
# cumprod：对数组中全部或者某个轴向的元素求累计积。零长度的数组返回零长度数组
arr = randn(3, 2)
print("arr =")
print(arr)
print("arr.mean() =", arr.mean())
print("np.mean(arr) =", np.mean(arr))
print("arr.mean(axis = 1) =", arr.mean(axis = 1))
print("np.mean(arr,axis = 1) =", np.mean(arr, axis = 1))

print("arr.sum() =", arr.sum())
print("arr.cumsum(axis = 0) =")
print(arr.cumsum(axis = 0))
print("arr.cumsum() =", arr.cumsum())

print("arr.cumprod(axis = 0) =")
print(arr.cumprod(axis = 0))
print("arr.cumprod() =", arr.cumprod())

# ch040303. 用于布尔型数组的方法
arr = randn(100)
print("(arr>0).sum() =", (arr > 0).sum())  # 正值的数量
bools = np.array([False, False, True, False])
bools.any()  # 数组中是否存在True
bools.all()  # 数组中是否不存在False

# ch040304. 排序
# 1. 数组排序
arr = randn(8)
print("arr =", arr)
arr.sort()
print("arr.sort() =", arr)

# 2. 多维数组某个轴排序
arr = randn(4, 3, 2)
print("arr =")
print(arr)
arr.sort(axis = 0)
print("arr.sort(axis = 0) =")
print(arr)

arr = randn(4, 3, 2)
print("arr =")
print(arr)
arr.sort(axis = 2)
print("arr.sort(axis = 2) =")
print(arr)

# 计算数组分位数的技巧
large_arr = randn(1000)
large_arr.sort()
print("5%分位数 =", large_arr[int(0.05 * len(large_arr))])

# 唯一化以及其他的集合逻辑
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
np.unique(names)
sorted(set(names))  # 等价代码

ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
np.unique(ints)

values = np.array([6, 0, 0, 3, 2, 5, 6])
np.in1d(values, [2, 3, 6])

# P107，表4-6：数组的集合运算
# unique(x)：计算x中的唯一元素，返回排序后的结果
# intersect1d(x,y)：计算x和y的交集（公共元素），返回排序后的结果
# union1d(x,y)：计算x和y的并集，
# in1d(x,y)：得到一个表示“x的元素是否包含于y”的布尔型数组
# setdiff1d(x,y)：集合的差，即元素在x中且不在y中
# setxor1d(x,y)：集合的对称差（异或），即存在于一个数组中但是不同时存在于两个数组中的元素

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
