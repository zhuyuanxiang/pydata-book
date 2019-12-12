# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ipython_test.py
@Version    :   v0.1
@Time       :   2019-12-11 14:53
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec03，P53
@Desc       :   IPython：一种交互式计算和开发环境，%run 命令
@理解
"""
import numpy as np
import winsound

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 3, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 通过设定种子确保每次运行时产生稳定的随机数字，从而简化验证的结果


# ----------------------------------------------------------------------
def f(x, y, z):
    return (x + y) / z


a, b, c = 5, 6, 7.5
result = f(a, b, c)
print("result =", result)
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
