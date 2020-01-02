# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1201_ndarray对象.py
@Version    :   v0.1
@Time       :   2019-12-30 17:03
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1201，P368
@Desc       :   NumPy 高级应用，ndarray 对象的内部机理
@理解：ndarray 内部组成：
1. 一个指向数组（一个系统内存块）的指针；
2. 数据类型或者 dtype
3. 一个表示数组形状（shape）的元组
4. 一个跨度元组（stride），其中的整数表示前进到当前维度下一个元素需要“跨过”的字节数

"""
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import winsound

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
# NumPy 数据类型体系
# np.integer 和 np.floating 是两个超类
ints = np.ones(10, dtype = np.uint16)
print(np.issubdtype(ints.dtype, np.integer))
floats = np.ones(10, dtype = np.float32)
print(np.issubdtype(floats.dtype, np.floating))

# dtype 的 mro() 可以查看所有的父类
pp(np.float64.mro())

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
