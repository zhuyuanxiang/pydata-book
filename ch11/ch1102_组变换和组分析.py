# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1102_组变换和组分析.py
@Version    :   v0.1
@Time       :   2019-12-30 11:38
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1102，P355
@Desc       :   金融和经济数据应用，组变换和组分析
@理解
"""
import random
import string
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame, Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
random.seed(0)


# ----------------------------------------------------------------------
def ch110200_组变换():
    def rands(n):
        choices = string.ascii_uppercase
        return ''.join([random.choice(choices) for _ in range(n)])

    N = 1000  # 随机生成1000个股票代码
    tickers = np.array([rands(5) for _ in range(N)])
    M = 500  # 创建含有 3 列的 DataFrame 来构建虚拟数据
    df = DataFrame({
            'Momentum': np.random.randn(M) / 200 + 0.03,
            'Value': np.random.randn(M) / 200 + 0.08,
            'ShortInterest': np.random.randn(M) / 200 - 0.02
    }, index = tickers[:M])

    # 为这些股票随机分配行业分类
    ind_names = np.array(['FINANCIAL', 'TECH'])
    sampler = np.random.randint(0, len(ind_names), N)
    industries = Series(ind_names[sampler], index = tickers, name = 'industry')
    by_industry = df.groupby(industries)
    show_title("根据行业分类进行分组聚合和变换")
    pp(by_industry.mean())
    pp(by_industry.describe())

    def zscore(group):
        return (group - group.mean()) / group.std()

    df_stand = by_industry.apply(zscore)
    show_title("分组内标准化处理")
    pp(df_stand)
    show_title("分组内标准化处理的意义（均值为0，方差为1）")
    pp(round(df_stand.groupby(industries).agg(['mean', 'std'])))

    # ToDo:看不懂到底以什么进行了排序
    ind_rank = by_industry.rank(ascending = True)
    show_title("分组内降序排名")
    pp(ind_rank)
    show_title("分组内降序排名的意义（最小值在后，最小值在前）")
    pp(ind_rank.groupby(industries).agg(['min', 'max']))

    show_title("行业内排名和标准化")
    pp(by_industry.apply(lambda x: zscore(x.rank())))


def ch110201_因子分析():
    # 因子分析（Factor Analysis）：是投资组合宣管理中的一种技术。
    # 投资组合的持有量和性能（收益和损失）可以被分解为一个或者多个表示投资组合权重的因子（风险因子就是其中之一）。
    # Beta风险系数：是一种常见的风险因子，表示某只股票的价格与某个基准（例如：标准普尔500指数）的协动性。
    def rands(n):
        choices = string.ascii_uppercase
        return ''.join([random.choice(choices) for _ in range(n)])

    N = 1000  # 随机生成1000个股票代码
    tickers = np.array([rands(5) for _ in range(N)])
    M = 500  # 创建含有 3 列的 DataFrame 来构建虚拟数据
    df = DataFrame({
            'Momentum': np.random.randn(M) / 200 + 0.03,
            'Value': np.random.randn(M) / 200 + 0.08,
            'ShortInterest': np.random.randn(M) / 200 - 0.02
    }, index = tickers[:M])

    factor1, factor2, factor3 = np.random.randn(3, 1000)
    # stock ticker：股票代码
    ticker_subset = tickers.take(np.random.permutation(N)[:1000])
    # 因子加权和 + 噪声
    port = Series(
        0.7 * factor1 - 1.2 * factor2 + 0.3 * factor3 + np.random.rand(1000),
        index = ticker_subset)
    factors = DataFrame(
            {'factor1': factor1, 'factor2': factor2, 'factor3': factor3},
            index = ticker_subset)
    show_title("各个因子与投资组合之间的矢量相关性")
    pp(factors.corrwith(
        port))  # ToDo: 因为最小二乘回归函数已经改变，所以这里先不修改了。  # pp(sm.ols(y = port, x = factors).beta)


def ch110202_四分位和十分位分析():
    # ToDo: 因为涉及较多的业务知识，所以这里先不修改了。
    # 因为修改需要两种能力：
    # 1. 对两种版本的 Pandas 很熟悉
    # 2. 对业务知识很熟悉
    # 而这样的能力对于学习 Pandas 并不是最重要的，因此暂时放弃修改。
    spx = pd.read_csv('stock_px.csv', parse_dates = True, index_col = 0).loc[
          '2011-09-05':'2011-09-14']['SPX']
    returns = spx.pct_change()

    def to_index(rets):
        index = (1 + rets).cumprod()
        first_loc = max(index.notnull().argmax() - 1, 0)
        index.values[first_loc] = 1
        return index

    def trend_signal(rets, lookback, lag):
        signal = rets.rolling(lookback, min_periods = lookback - 5).sum()
        return signal.shift(lag)

    signal = trend_signal(returns, 100, 3)
    trade_friday = signal.resample('W-FRI').ffill().resample('B').ffill()
    trade_rets = trade_friday.shift(1) * returns

    to_index(trade_rets).plot()
    plt.title("图11-1：SPY 动量策略收益指数")
    plt.show()


# ToDo：后面几个都与业务联系较多，先放弃修改。

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
