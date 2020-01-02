# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1007_时间序列绘图.py
@Version    :   v0.1
@Time       :   2019-12-29 16:11
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1007，P334
@Desc       :   时间序列，时间序列绘图
@理解
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
close_px_all = pd.read_csv('../ch09/stock_px.csv', parse_dates = True,
                           index_col = 0)
show_title("close_px_all")
pp(close_px_all)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
close_px = close_px.resample('B').ffill()  # 补充缺失的工作日数据
show_title("close_px")
pp(close_px)

close_px['AAPL'].plot()
plt.title("图10-4：苹果公司每日股价")
plt.show()
close_px.loc['2009'].plot()
plt.title("图10-5：2009 年三个公司的每日股价")
plt.show()
close_px['AAPL'].loc['01-2011':'03-2011'].plot()
plt.title("图10-6：苹果公司在 2011 年 1 月到 3 月间的每日股价")
plt.show()
close_px['AAPL'].resample('Q-DEC').ffill().loc['2009'].plot()
plt.title("图10-6：苹果公司在 2009 年到 2011 年间的每季度股价")
plt.show()
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
