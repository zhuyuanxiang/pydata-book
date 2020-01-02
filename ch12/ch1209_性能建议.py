# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1209_性能建议.py
@Version    :   v0.1
@Time       :   2020-01-02 8:59
@License    :   (C)Copyright 2018-2020, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1209，P397
@Desc       :   NumPy 高级应用，性能建议
@理解：其他加速手段（Cython
"""
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import winsound

# 设置数据显示的精确度为小数点后4位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch120901_连续内存():
    arr_c = np.ones((100, 100), order = 'C')
    print("arr_c.flags =", arr_c.flags)

    arr_f = np.ones((100, 100), order = 'F')
    print("arr_f.flags =", arr_f.flags)
    print("arr_f.flags.f_contiguous =", arr_f.flags.f_contiguous)
    print("arr_f.flags =", arr_f.copy('C').flags)

    print("构造数组时，内存中可能是连续的：", arr_c[:50].flags.contiguous)
    print("构造视力时，在内存中可能是不连续的：", arr_c[:, 50].flags.contiguous)


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
