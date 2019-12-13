# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0402_functions.py
@Version    :   v0.1
@Time       :   2019-12-12 9:45
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0402，P98
@Desc       :   NumPy基础：数组和矢量计算，通用函数：快速的元素级数组函数
@理解：
"""
import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from pprintpp import pprint as pp

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
# 通用函数（ufunc）是一种对ndarray中的数据执行元素级运算的函数。
# 也可以将其看作简单函数的矢量化包装器，可以接受一个或者多个标量值，产生一个或者多个标量值
# 一元通用函数（unary ufunc）：P99，表4-3：一元ufunc
# abs, fabs：计算绝对值，fabs不支持复数，abs全部支持｛abs(1+1j)｝
# sqrt：计算各元素的平方根，等价于arr**0.5
# square：计算各元素的平方，等价于arr**2
# exp：计算各元素的指数
# log, log10, log2, log1p：计算各元素的对数
# sign：计算各元素的指示函数
# ceil：计算各元素的向上取整
# floor：计算各元素的向下取整
# rint：计算各元素的四舍五入，保留dtype
# modf：将数组的小数和整数分成两个独立数组的形式返回
# isnan：计算各元素的布尔值（判断哪些值是NaN）
# isfinite, isinf：计算各元素的布尔值（判断哪些元素是有穷的finite和无穷的inf）
# cos, cosh, sin, sinh, tan, tanh：三角函数
# arccos, arccosh, arcsin, arcsinh, arctan, arctanh：反三角函数
# logical_not：计算各元素取非的真值
arr = np.arange(0, 5, 0.3)
print("arr =", arr)

print("np.sqrt(arr) =")
pp(np.sqrt(arr))

print("np.exp(arr)")
pp(np.exp(arr))

print("np.modf(arr) =", np.modf(arr))
# 二元通用函数（binary ufunc）：P100，表4-4：二元ufunc
# add：数组中对应的元素相加
# subtract：从第一个数组中减去第二个数组中的元素
# multiply：数组元素相乘
# divide, floor_divide：数组元素相除和向下圆整除法（丢弃余数）
# power：数组中对应的元素取幂
# maximum, fmax：数组中对应的元素取最大值，忽略NaN
# minimum, fmin：数组中对应的元素取最小值，忽略NaN
# mod：数组中对应的元素求模（除法的余数）
# copysign：计算第二个数组中元素的指示函数，将其结果乘以第一个数组中的对应元素
# greater, greater_equal, less, less_equal, equal, not_equal：数组中对应的元素的布尔运算
# logical_and, logical_or, logical_xor：数组中对应的元素的真值逻辑运算，相当于中缀运算符&、|、^
from numpy.random import randn

x, y = randn(8), randn(8)
print("x =", x)
print("y =", y)
print("np.maximum(x, y) =", np.maximum(x, y))

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
