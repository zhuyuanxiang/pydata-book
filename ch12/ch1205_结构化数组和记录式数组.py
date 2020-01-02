# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1205_结构化数组和记录式数组.py
@Version    :   v0.1
@Time       :   2019-12-31 17:25
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1205，P386
@Desc       :   NumPy 高级应用，结构化数组和记录式数组
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
# 结构化数组：特殊的ndarray，其中的各个元素可以被看作 C 语言中的结构体或者 SQL 表中带有多个命名字段的行
dtype = [('x', np.float64), ('y', np.int32)]
sarr_结构化数组 = np.array([(1.5, 6), (np.pi, -2)], dtype = dtype)
show_title("sarr_结构化数组")
pp(sarr_结构化数组)

show_title("数组的元素是元组式对象")
print("sarr_结构化数组[0] =", sarr_结构化数组[0])

show_title("访问结构化数组的某个字段时，返回的是该数据的视图")
print("sarr_结构化数组['x'] =", sarr_结构化数组['x'])

print("sarr_结构化数组[0]['y'] =", sarr_结构化数组[0]['y'])

# 多维字段
dtype = [('x', np.int64, 3), ('y', np.int32)]
arr = np.zeros(4, dtype = dtype)
show_title("arr")
pp(arr)

print("arr[0]['x'] =", arr[0]['x'])

show_title("arr['x']")
pp(arr['x'])

# 嵌套 dtype
dtype = [('x', [('a', 'f8'), ('b', 'f4')]), ('y', np.int32)]
data = np.array([((1, 2), 5), ((3, 4), 6)], dtype = dtype)
pp(data)
pp(data['x'])
pp(data['y'])
pp(data['x']['a'])

# 为什么要使用结构化数组？
# 1. 将单个内存块解释为带有任意复杂嵌套列的表格型结构，可以提供快速高效的数据读写
# 2. 将数据文件写成定长记录的字节流，即C和C++代码中常见的数据序列化手段

# 结构化数组操作：numpy.lib.recfunctions
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
