# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0903_group_wise.py
@Version    :   v0.1
@Time       :   2019-12-26 17:19
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0903，P276
@Desc       :   数据取聚合与分组运算，分组级运算和转换
@理解：聚合：是数据转换的特例，将一维数组简化为标量值的函数。
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame, Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
def ch090300_transform():
    df = DataFrame({
            'key1': ['a', 'a', 'b', 'b', 'a'],
            'key2': ['one', 'two', 'one', 'two', 'one'],
            'data1': np.random.randn(5), 'data2': np.random.randn(5)
    })
    show_title("原始数据")
    pp(df)

    k1_means = df.groupby('key1').mean().add_prefix('mean_')
    pp(k1_means)
    show_title("添加一个用于存放各个索引分组平均值的列")
    pp(pd.merge(df, k1_means, left_on = 'key1', right_index = True))

    people = DataFrame(np.random.randn(5, 5),
                       columns = ['a', 'b', 'c', 'd', 'e'],
                       index = ['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
    people.loc[2:3, ['b', 'c']] = np.nan
    show_title("原始数据")
    pp(people)

    key = ['one', 'two', 'one', 'two', 'one']
    pp(people.groupby(key).mean())
    show_title("transfor()实现两类关键字的映射转换")
    pp(people.groupby(key).transform(np.mean))

    # 距离平均化函数
    def demean(arr):
        return arr - arr.mean()

    show_title("自定义函数的转换")
    demeaned = people.groupby(key).transform(demean)
    pp(demeaned)
    pp(demeaned.groupby(key).mean())


# ch090301. apply：一般性的“拆分——应用——合并”
def ch090301_拆分_应用_合并():
    # 选取指定列中含有最大值的行数据的函数
    def top(df, n = 5, column = 'tip_pct'):
        return df.sort_values(by = column)[-n:]

    tips = pd.read_csv('../ch08/tips.csv')

    # Add tip percentage of total bill（小费占总额的百分比）
    tips['tip_pct'] = tips['tip'] / tips['total_bill']
    show_title("原始数据")
    pp(tips.head())
    pp(top(tips, n = 6))
    pp(tips.groupby('smoker').apply(top))
    pp(tips.groupby(['smoker', 'day']).apply(top, n = 1, column = 'total_bill'))
    pp(tips.groupby('smoker')['tip_pct'].describe())
    pp(tips.groupby('smoker')['tip_pct'].describe().unstack('smoker'))

    grouped = tips.groupby(['sex', 'smoker'])
    f = lambda x: x.describe()
    pp(grouped.apply(f))

    # ch09030101. 禁止分组键
    pp(tips.groupby('smoker', group_keys = True).apply(top))
    show_title("禁止分组键和原始对象的索引共同构成结果对象中的层次化索引")
    pp(tips.groupby('smoker', group_keys = False).apply(top))


# ch090302. 分位数（quantile）和桶（bucket）分析
def ch090302_分位数_桶分析():
    frame = DataFrame(
            {'data1': np.random.randn(1000), 'data2': np.random.randn(1000)})
    factor = pd.cut(frame.data1, 4)
    show_title("原始数据")
    pp(factor.values)
    pp(factor.cat.categories)

    def get_stats(group):
        return {
                'min': group.min(), 'max': group.max(), 'count': group.count(),
                'mean': group.mean()
        }

    show_title("对 cut 返回的对象做统计")
    grouped = frame.data2.groupby(factor)
    pp(grouped.apply(get_stats).unstack())

    show_title("根据样本分位数得到大小相等的桶")
    grouping = pd.qcut(frame.data1, 10, labels = False)
    grouped = frame.data2.groupby(grouping)
    pp(grouped.apply(get_stats).unstack())


def ch090303_使用特定于分组的值填充缺失值():
    series = Series(np.random.randn(6))
    series[::2] = np.nan
    show_title("原始数据")
    pp(series)
    print("series.mean() =", series.mean())
    show_title("使用特定于分组的值填充缺失值")
    pp(series.fillna(series.mean()))

    states = ['Ohio', 'New York', 'Vermont', 'Florida', 'Oregon', 'Nevada',
              'California', 'Idaho']
    group_key = ['East'] * 4 + ['West'] * 4
    data = Series(np.random.randn(8), index = states)
    data[['Vermont', 'Nevada', 'Idaho']] = np.nan
    show_title("原始数据")
    pp(data)
    print("data.mean() =", data.mean())
    show_title("使用特定于分组的值填充缺失值")
    pp(data.fillna(data.mean()))

    show_title("预定义各个分组的填充值")
    fill_values = {'East': 0.5, 'West': -1}
    fill_func = lambda g: g.fillna(fill_values[g.name])
    pp(data.groupby(group_key).apply(fill_func))


def ch090304_随机采样和排列():
    # 红桃（Hearts）、黑桃（Spades）、梅花（Clubs）、方片（Diamonds）
    suits = ['H', 'S', 'C', 'D']
    # suits = ['红桃', '黑桃', '梅花', '方片']
    card_val = ([x for x in range(1, 11)] + [10] * 3) * 4
    base_names = ['A'] + [x for x in range(2, 11)] + ['J', 'Q', 'K']
    cards = []
    for suit in suits:
        cards.extend(str(num) + suit for num in base_names)
        pass
    deck = Series(card_val, index = cards)
    show_title("抽取前13张牌")
    pp(deck[:13])

    def draw(deck, n = 5):
        return deck.take(np.random.permutation(len(deck))[:n])

    show_title("随机抽取5张牌")
    pp(draw(deck))

    get_suit = lambda card: card[-1]
    show_title("从每种花色中随机抽取两张牌")
    pp(deck.groupby(get_suit).apply(draw, n = 2))
    show_title("从每种花色中随机抽取两张牌（不分组）")
    pp(deck.groupby(get_suit, group_keys = False).apply(draw, n = 2))


def ch090305_example_分组加权平均数和相关系数():
    df = DataFrame({
            'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
            'data': np.random.randn(8), 'weights': np.random.randn(8)
    })
    show_title("原始数据")
    pp(df)

    grouped = df.groupby('category')
    get_加权平均数 = lambda g: np.average(g['data'], weights = g['weights'])
    show_title("计算分组的加权平均数")
    pp(grouped.apply(get_加权平均数))

    close_标准普尔500指数 = pd.read_csv('stock_px.csv', parse_dates = True,
                                  index_col = 0)
    show_title("原始数据")
    pp(close_标准普尔500指数)

    rets_百分数变化 = close_标准普尔500指数.pct_change().dropna()
    spx_年度相关系数 = lambda x: x.corrwith(x['SPX'])

    def func_year(x):
        print("x =", x)
        print("x.year =", x.year)
        return lambda x: x.year

    by_year = rets_百分数变化.groupby(func_year)
    by_year = rets_百分数变化.groupby(lambda x: x.year)

    show_title("苹果 和 微软 的年度相关系数")
    pp(by_year.apply(lambda g: g['AAPL'].corr(g['MSFT'])))


def ch090306_example_面向分组的线性回归():
    import statsmodels.api as sm

    def regress(data, yvar, xvars):
        Y = data[yvar]
        X = data[xvars]
        X['intercept'] = 1.
        # OLS(Ordinary Least Squares, 普通最小二乘法)
        result = sm.OLS(X, Y).fit()
        return result.params

    close_标准普尔500指数 = pd.read_csv('stock_px.csv', parse_dates = True,
                                  index_col = 0)
    show_title("原始数据")
    pp(close_标准普尔500指数)

    rets_百分数变化 = close_标准普尔500指数.pct_change().dropna()
    spx_年度相关系数 = lambda x: x.corrwith(x['SPX'])
    year_分组 = rets_百分数变化.groupby(lambda x: x.year)
    show_title("按年计算 AAPL 对 SPX 收益率的线性回归")
    pp(year_分组.apply(regress, 'AAPL', ['SPX']))


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
