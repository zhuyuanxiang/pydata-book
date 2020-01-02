# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0802_pandas_plot.py
@Version    :   v0.1
@Time       :   2019-12-25 8:14
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0802，P244
@Desc       :   绘图和可视化，pandas 中的绘图函数
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame, Series
from pandas.plotting import scatter_matrix

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch080201. 线型图
def ch080201_linear():
    # P246，表8-3：Series.plot 方法的参数
    # 1. label：图例的标签
    # 2. ax：用于绘制 matplotlib.subplot 对象
    # 3. style：风格字符串
    # 4. alpha：填充不透明度
    # 5. kind：图表风格（line, bar, barh, kde）
    # 6. logy：在 Y 轴上使用对数标尺
    # 7. use_index：将对象的索引用于刻度标签
    # 8. rot：旋转刻度标签的度数
    # 9. xticks, yticks：X轴 或者 Y轴 的刻度值
    # 10. xlim, ylim：X轴或者 Y轴的界限
    # 11. grid：显示轴的网格线。默认（True）
    series = Series(np.random.randn(10).cumsum(), index = np.arange(0, 100, 10))
    series.plot()

    # P247，表8-4：DataFrame.plot 方法的独有的参数
    # 1. subplots：将各个DataFrame列绘制到单独的 subplot 中
    # 2. sharex, sharey：共用相同的 X轴 或者 Y轴，包括：刻度和界限
    # 3. figsize：表示图像大小的元组
    # 4. title：表示图像标量的字符串
    # 5. legend：添加一个 subplot 图例。默认（True）
    # 6. sort_columns：以字母表的顺序绘制各列。默认（当前列顺序）
    df = DataFrame(np.random.randn(10, 4).cumsum(0),
                   columns = ['A', 'B', 'C', 'D'],
                   index = np.arange(0, 100, 10))
    df.plot()


# ch080202. 柱状图
def ch080202_bar():
    fig, axes = plt.subplots(2, 1)
    series = Series(np.random.randn(16), index = list('abcdefghijklmnop'))
    series.plot(kind = 'bar', ax = axes[0], color = 'k', alpha = 0.7)
    series.plot(kind = 'barh', ax = axes[1], color = 'k', alpha = 0.7)

    df = DataFrame(np.random.randn(6, 4),
                   index = ['one', 'two', 'three', 'four', 'five', 'six'],
                   columns = pd.Index(['A', 'B', 'C', 'D'], name = 'Genus'))
    pp(df)
    df.plot(kind = 'bar')
    df.plot(kind = 'barh', stacked = True, alpha = 0.5)

    tips = pd.read_csv('tips.csv')
    show_title("原始数据")
    pp(tips.head())
    party_counts = pd.crosstab(tips.day, tips.scale)
    show_title("交叉表")
    pp(party_counts)
    # 因为1个人和6个人的取值都比较少见，所以剔除
    party_counts = party_counts.loc[:, 2:5]
    # 将结果“归一化”
    party_pcts = party_counts.div(party_counts.sum(1).astype(float), axis = 0)
    pp(party_pcts)
    party_pcts.plot(kind = 'bar', stacked = True, title = "图8-18：每天各种聚会规模的比例")


# ch080203. 直方图和密度图
def ch080203_histogram_density():
    tips = pd.read_csv('tips.csv')
    tips['tip_pct'] = tips['tip'] / tips['total_bill']
    tips['tip_pct'].hist(bins = 50)  # 直方图
    tips['tip_pct'].plot(kind = 'kde')  # 密度图
    plt.title("图8-20：小费百分比的直方图和密度图")

    comp1 = np.random.normal(0, 1, size = 200)  # N(0,1)
    comp2 = np.random.normal(10, 2, size = 200)  # N(10,2)
    values = Series(np.concatenate([comp1, comp2]))
    values.hist(bins = 100, alpha = 0.3, color = 'k', normed = True)
    values.plot(kind = 'kde', style = 'k--')
    pass


# ch080204. 散布图
def ch080204_scatter():
    macro = pd.read_csv('macrodata.csv')
    data = macro[['cpi', 'm1', 'tbilrate', 'unemp']]
    trans_data = np.log(data).diff().dropna()
    pp(trans_data[-5:])
    plt.scatter(trans_data['m1'], trans_data['unemp'])
    plt.title("图8-22：Changes in log {} vs. log {}".format('m1', 'unemp'))

    scatter_matrix(trans_data, diagonal = 'kde', color = 'k', alpha = 0.3)
    pass


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
