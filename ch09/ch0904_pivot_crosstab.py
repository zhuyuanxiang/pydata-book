# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0904_pivot_crosstab.py
@Version    :   v0.1
@Time       :   2019-12-27 11:20
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0904，P288
@Desc       :   数据取聚合与分组运算，透视表和交叉表
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch090400_透视表():
    # P290，表9-2：pivot_table 的参数
    # 1. values：待聚合的列的名称。默认（聚合所有数值列）
    # 2. index：用于分组的列名或者其他分组键，出现在结果透视表的行
    # 3. columns：用于分组的列名或者其他分组键，出现在结果透视表的列
    # 4. aggfunc：聚合函数或者函数列表，默认（'mean'）
    # 5. fill_value：用于替换结果表中的缺失值
    # 6. margins：添加行/列小计和总计，默认（False）
    tips = pd.read_csv('../ch08/tips.csv')

    # Add tip percentage of total bill（小费占总额的百分比）
    tips['tip_pct'] = tips['tip'] / tips['total_bill']
    show_title("原始数据")
    pp(tips.head())
    show_title("根据 sex 和 smoker 计算分组平均数")
    pp(tips.pivot_table(index = ['sex', 'smoker']))

    show_title("聚合tip_pct 和 size，根据 day 分组")
    pp(tips.pivot_table(['tip_pct', 'scale'], index = ['sex', 'day'],
                        columns = 'smoker'))

    show_title("聚合tip_pct 和 size，根据 day 分组，添加分项小计")
    pp(tips.pivot_table(['tip_pct', 'scale'], index = ['sex', 'day'],
                        columns = 'smoker', margins = True))

    pp(tips.pivot_table(['scale'], index = ['time', 'sex', 'smoker'],
                        columns = 'day', aggfunc = 'sum'))
    show_title("聚合tip_pct 和 size，根据 day 分组，添加分项小计，设置NA的填充值")
    pp(tips.pivot_table(['scale'], index = ['time', 'sex', 'smoker'],
                        columns = 'day', aggfunc = 'sum', fill_value = 0))


# ch090401. cross tabulation，交叉表：用于计算分组频率的特殊透视表.
def ch090401_cross_tabulation_交叉表():
    from io import StringIO

    data = """\
    Sample    Gender    Handedness
    1    Female    Right-handed
    2    Male    Left-handed
    3    Female    Right-handed
    4    Male    Right-handed
    5    Male    Left-handed
    6    Male    Right-handed
    7    Female    Right-handed
    8    Female    Left-handed
    9    Male    Right-handed
    10    Female    Right-handed"""
    data = pd.read_table(StringIO(data), sep = '\s+')
    pd.crosstab(data.Gender, data.Handedness, margins = True)

    tips = pd.read_csv('../ch08/tips.csv')
    pd.crosstab([tips.time, tips.day], tips.smoker, margins = True)


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
