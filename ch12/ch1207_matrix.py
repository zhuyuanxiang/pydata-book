# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1207_matrix.py
@Version    :   v0.1
@Time       :   2020-01-02 8:32
@License    :   (C)Copyright 2018-2020, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1207，P393
@Desc       :   NumPy 高级应用，NumPy 的 Matrix 类
@理解：Python的矩阵处理比较繁琐，当然3.7的版本提高了许多
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
X = np.array([[8.83, 3.82, -1.14, 2.04], [3.82, 6.75, 0.84, 2.08],
              [-1.14, 0.84, 5.02, 0.80], [2.04, 2.08, 0.80, 6.24]])

show_title("X")
pp(X)
show_title("X[:, 0]")
pp(X[:, 0])
y = X[:, :1]
show_title("y")
pp(y)

show_title("y^T X y")
pp(np.dot(y.T, np.dot(X, y)))
pp(y.T @ (X @ y))

# Python 3.5 开始就开始废弃 matrix 类
# https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html
X_matrix = np.matrix(X)
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
