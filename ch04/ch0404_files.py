# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0404_files.py
@Version    :   v0.1
@Time       :   2019-12-12 16:58
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0404，P107
@Desc       :   NumPy基础：数组和矢量计算，用于数组的文件输入输出
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from numpy.random import randn

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
# 1. 将数组以二进制格式保存在磁盘
arr = np.arange(10)
print("arr =", arr)
np.save('some_array.npy', arr)
next_arr = np.load('some_array.npy')[::-1]
print("next_arr =", next_arr)
np.savez('array_archive.npz', a = arr, b = next_arr)
arch = np.load('array_archive.npz')
print("arch['b']", arch['b'])

# 2. 存取文本文件
# !more array_ex.txt    # windows 环境下执行这个命令
arr = np.loadtxt('array_ex.txt', delimiter = ',')
print("arr =")
pp(arr)
np.savetxt('array_ex_new.txt', arr, delimiter = ',')

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
