# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1008_移动窗口函数.py
@Version    :   v0.1
@Time       :   2019-12-29 16:37
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1008，P337
@Desc       :   时间序列，
移动窗口函数（Moving Window Function）指的是在移动窗口（可以带有指数衰减权数）上计算各种统计函数
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
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样

# ----------------------------------------------------------------------
# P339，表10-6：移动窗口和指数加权函数（rolling_xxx()已经在0.18版本被废弃）
close_px_all = pd.read_csv('../ch09/stock_px.csv', parse_dates = True,
                           index_col = 0)
show_title("close_px_all")
pp(close_px_all)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
close_px = close_px.resample('B').ffill()  # 补充缺失的工作日数据
show_title("close_px")
pp(close_px)


def ch100800_移动窗口():
    close_px.AAPL.plot()
    close_px.AAPL.rolling(250).mean().plot()
    plt.title("图10-8：苹果公司股价的 250 日均线")
    plt.show()

    close_px.AAPL.rolling(250, min_periods = 10).std().plot()
    plt.title("图10-9：苹果公司 250 日每日回报标准差")
    plt.show()

    close_px.rolling(60).mean().plot(logy = True)
    plt.title("图10-10：各个股价的 60 日均线（Y轴是对数刻度）")
    plt.show()

    # 计算扩展窗口平均（Expanding Window Mean）
    # expanding_mean = lambda x: x.rolling(len(x), min_periods = 1).mean()
    close_px.expanding(min_periods = 1).mean().plot(logy = True)
    plt.show()


def ch100801_指数加权函数():
    fig, axes = plt.subplots(nrows = 2, ncols = 1, sharex = True, sharey = True,
                             figsize = (12, 7))
    aapl_px = close_px.AAPL['2005':'2009']
    ma60 = aapl_px.rolling(60, min_periods = 50).mean()
    ewma60 = aapl_px.ewm(span = 60).mean()

    aapl_px.plot(style = 'k-', ax = axes[0])
    ma60.plot(style = 'k--', ax = axes[0])
    axes[0].set_title('Simple MA')
    aapl_px.plot(style = 'k-', ax = axes[1])
    ewma60.plot(style = 'k--', ax = axes[1])
    axes[1].set_title("Exponentially-weighted MA")
    plt.show()


def ch100802_二元移动窗口函数():
    spx_px = close_px_all['SPX']
    spx_rets = spx_px / spx_px.shift(1) - 1
    spx_rets = spx_px.pct_change()
    returns = close_px.pct_change()
    corr = returns.AAPL.rolling(125, min_periods = 100).corr(spx_rets)
    corr.plot()
    plt.title("图10-12：AAPL 6个月的回报与标准普尔500指数的相关系数")
    plt.show()

    corr = returns.rolling(125, min_periods = 100).corr(spx_rets)
    corr.plot()
    plt.title("图10-13：3只股票6个月的回报与标准普尔500指数的相关系数")
    plt.show()
    pass


def ch100803_用户定义的移动窗口函数():
    from scipy.stats import percentileofscore
    returns = close_px.pct_change()
    score_at_2percent = lambda x: percentileofscore(x, 0.02)
    result = returns.AAPL.rolling(250).apply(score_at_2percent, raw = True)
    result.plot()
    plt.title("图10-14：AAPL 2% 的回报率的百分等级（一年窗口期）")
    plt.show()
    pass


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
