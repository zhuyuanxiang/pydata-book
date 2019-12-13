# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0405_linear_algebra.py
@Version    :   v0.1
@Time       :   2019-12-12 17:14
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0405，P109
@Desc       :   NumPy基础：数组和矢量计算，线性代数
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
x = np.array([[1., 2., 3.], [4., 5., 6.]])
y = np.array([[6., 23.], [-1, 7], [8, 9]])
print("x =")
pp(x)
print("y =")
pp(y)
print('-' * 5, "矩阵乘以矩阵", '-' * 5)
print("x.dot(y) =")
pp(x.dot(y))
print("np.dot(x,y) =")
pp(np.dot(x, y))

print('-' * 5, "矩阵乘以向量", '-' * 5)
print("np.dot(x, np.ones(3)) =")
pp(np.dot(x, np.ones(3)))

# P110，表4-7：常用的 numpy.linalg 函数
# diag：以一维数组的形式返回方阵的对角线（或非对角线）元素，或将一维数组转换为方阵（非对角线元素为0）
# dot：矩阵乘法
# trace：方阵的迹（方阵对角线元素的和）
# det：方阵行列式
# eig：方阵的本征值和本征向量
# inv：方阵的逆
# pinv：矩阵的Moore-Penrose伪逆
# qr：QR分解
# svd：奇异值分解
# solve：解线性方程组 Ax=b，其中A为一个方阵
# lstsq：计算Ax=b的最小二乘解
print('-' * 5, "numpy.linalg中常用函数", '-' * 5)
from numpy.linalg import inv, qr
from numpy.random import randn

X = randn(5, 5)
mat = X.T.dot(X)
print("inv(mat) =")
pp(inv(mat))
print("mat.dot(inv(mat)) =")
pp(mat.dot(inv(mat)))
print("qr(mat) =")
pp(qr(mat))

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
