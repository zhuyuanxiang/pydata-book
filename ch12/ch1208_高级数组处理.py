# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1208_高级数组处理.py
@Version    :   v0.1
@Time       :   2020-01-02 8:47
@License    :   (C)Copyright 2018-2020, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1208，P395
@Desc       :   NumPy 高级应用，高级数组的输入和输出
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
def ch120801_内存映像文件():
    # 内存映像（Memory Map）：读取内存中放不下的数据集。
    # 结构化存取保存在硬盘上的数据文件
    mmap = np.memmap('mymmap', dtype = 'float64', mode = 'w+',
                     shape = (100, 100))
    show_title("mmap")
    pp(mmap)

    section = mmap[:5]
    section[:] = np.random.randn(5, 100)
    del mmap

    mmap = np.memmap('mymmap', dtype = 'float64', shape = (100, 100))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
