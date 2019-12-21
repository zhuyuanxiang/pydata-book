# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0602_binary_data.py
@Version    :   v0.1
@Time       :   2019-12-20 18:08
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0602，P179
@Desc       :   数据加载、存储与文件格式，二进制数据格式
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import pandas as pd
import winsound

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# pickle 序列化：存储数据的二进制格式
def ch060200_pickle():
    data = pd.read_csv('ch06/ex1.csv')
    print('-' * 5, "使用 read_csv 读取的原始数据", '-' * 5)
    pp(data)

    data.to_pickle('ch06/data_pickle')
    pp(pd.read_pickle('ch06/data_pickle'))


# ch060201. HDF5 格式：文件系统式的节点结构，能够存储多个数据集并且支持元数据。
# 支持多种压缩器的即时压缩，还能存储重复模式数据。
# 可以高效地分块读写，方便处理那些非常大的无法直接放入内存的数据集。
# Python中的HDF5库中有两个接口：
#   - PyTables：抽象了HDF5的许多细节以提供多种灵活的数据容器、表索引、查询功能以及对核外计算技术的某些支持
#   - h5py：直接而高级的HDF5 API访问接口
# HDF(Hierarchical Data Format)：层次型数据格式
def ch060201_HDF5():
    data = pd.read_csv('ch06/ex1.csv')
    print('-' * 5, "使用 read_csv 读取的原始数据", '-' * 5)
    pp(data)

    store = pd.HDFStore('ch06/mydata.h5')
    store['obj1'] = data
    store['obj1_col'] = data['a']
    print('-' * 5, "使用 HDF5 存储的原始数据", '-' * 5)
    pp(store)
    pp(store['obj1'])
    pp(store['obj1_col'])
    pass


# ch060202. Excel 文件读取
def ch060202_excel():
    xls_file = pd.ExcelFile('ch06/data.xls')
    pp(xls_file)
    table = xls_file.parse('Sheet1')
    pp(table)


print('-' * 5, "", '-' * 5)
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
