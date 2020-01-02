# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0406_random_number.py
@Version    :   v0.1
@Time       :   2019-12-12 17:49
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec04006，P111
@Desc       :   NumPy基础：数组和矢量计算，随机数生成
@理解：
"""
from pprint import pprint as pp
from random import random
from timeit import timeit

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from numpy.random import randn

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
# P111，表4-8：部分 numpy.random 函数
# seed：随机数生成器的种子
# permutation：输入的序列返回这个序列的随机排列；
# 输入是数返回一个随机排列的范围，等价于输入一个范围，返回这个范围序列的随机排列
# shuffle：对一个序列就地随机排列
# rand：产生均匀分布的样本值
# randint：从给定的上下限范围内随机选取整数
# binomial：产生二项分布的样本值
# normal：产生正态分布的样本值（自定义均值和方差）
# randn：产生正态分布（平均值为0，标准差为1）的样本值
# beta：产生beta分布的样本值
samples = np.random.normal(size = (4, 4))
print("sampels =")
pp(samples)

run_str = """
from random import normalvariate
N = 1000000
samples =[normalvariate(0, 1) for _ in range(N)]
"""

timeit(run_str)

normal_str = """
import numpy as np
np.random.normal(size=10)"""
timeit(stmt = normal_str, number = 100000)

# 范例：随机漫步
position = 0
walk = [position]
steps = 1000
for i in range(steps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)
    pass
plt.plot(walk)
plt.title("图4-4：简单的随机漫步")

# 使用统计方法实现的随机漫步
nsteps = 1000
draws = np.random.randint(0, 2, size = nsteps)
steps = np.where(draws > 0, 1, -1)
walk = steps.cumsum()
plt.plot(walk)
plt.title("图4-4：简单的随机漫步")

walk.min()
walk.max()
(np.abs(walk) >= 10).argmax()

# 一次模拟多个随机漫步
nwalks = 5000
nsteps = 1000
draws = np.random.randint(0, 2, size = (nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
pp(walks)
walks.min()
walks.max()

hist30 = (np.abs(walks) >= 30).any(1)
pp(hist30)
pp(hist30.sum())

crossing_times = (np.abs(walks[hist30]) >= 30).argmax(1)
pp(crossing_times)
pp(crossing_times.mean())

nwalks = 50
draws = np.random.normal(0, 2, size = (nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
hist30 = (np.abs(walks) >= 30).any(1)
crossing_times = (np.abs(walks[hist30]) >= 30).argmax(1)
pp(crossing_times.mean())

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
