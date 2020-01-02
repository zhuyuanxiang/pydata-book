# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0801_primer.py
@Version    :   v0.1
@Time       :   2019-12-24 17:33
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0801，P231
@Desc       :   绘图和可视化，matplotlib API 入门
@理解：
"""
import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from numpy.random import randn

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch080101. Figure 和 Subplot
def ch080101_figure_subplot():
    # P235，表8-1：subplot()的参数
    # 1. nrows：subplot的行数
    # 2. ncols：subplot的列数
    # 3. sharex：所有 subplot 应该使用相同的X轴刻度
    # 4. sharey：所有 subplot 应该使用相同的Y轴刻度
    # 5. subplot_kw：用于创建各个 subplot 的关键字字典
    # 6. **fig_kw：创建 figure 时的其他关键字
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax1.hist(randn(100), bins = 20, color = 'k', alpha = 0.3)
    ax2.scatter(np.arange(30), np.arange(30) + 3 * randn(30))
    ax3.plot(randn(50).cumsum(), 'k--')

    fig, axes = plt.subplots(2, 2)
    axes[0, 0].hist(randn(100), bins = 20, color = 'k', alpha = 0.3)
    axes[0, 1].scatter(np.arange(30), np.arange(30) + 3 * randn(30))
    axes[1, 0].plot(randn(50).cumsum(), 'k--')

    # subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspaece=None)
    fig, axes = plt.subplots(2, 2, sharex = True, sharey = True)
    for i in range(2):
        for j in range(2):
            axes[i, j].hist(randn(500), bins = 50, color = 'k', alpha = 0.5)
            pass
        pass
    plt.subplots_adjust(wspace = 0, hspace = 0)


# ch080102. 颜色、标记和线型
def ch080102_colors_markers_line_styles():
    plt.figure()
    plt.plot(randn(30).cumsum(), 'ko--')
    data = randn(30).cumsum()
    plt.plot(data, 'k--', label = 'Default')
    plt.plot(data, 'k-', drawstyle = 'steps-post', label = 'steps-post')
    plt.legend(loc = 'best')


# ch080103. 刻度、标签和图例
def ch080103_ticks_labels_legends():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(randn(1000).cumsum())

    ticks = ax.set_xticks([0, 250, 500, 750, 1000])  # 设置刻度
    # set_xtickslabels() 没有这个属性
    labels = ax.set_xtickslabels(['one', 'two', 'three', 'four', 'five'],
                                 rotation = 30, fontsize = 'small')
    ax.set_title("我的第一个图")  # 设置标量
    ax.set_xlabel('Stages')  # 设置轴标签

    # 设置图例
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(randn(1000).cumsum(), 'k', label = 'one')
    ax.plot(randn(1000).cumsum(), 'k-', label = 'two')
    ax.plot(randn(1000).cumsum(), 'k.', label = 'three')
    ax.plot(randn(1000).cumsum(), 'k--', label = 'four')
    ax.legend(loc = 'best')


# ch080104. 注解和绘图
def ch080104_annotation_draw():
    from datetime import datetime

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    data = pd.read_csv('ch08/spx.csv', index_col = 0, parse_dates = True)
    spx = data['SPX']
    spx.plot(ax = ax, style = 'k-')

    crisis_data = [(datetime(2007, 10, 11), 'Peak of bull market'),
            (datetime(2008, 3, 12), 'Bear Stearns Fails'),
            (datetime(2008, 9, 15), 'Lehman Bankruptcy')]
    # 注解
    for date, label in crisis_data:
        ax.annotate(label, xy = (date, spx.asof(date) + 50),
                    xytext = (date, spx.asof(date) + 200),
                    arrowprops = dict(facecolor = 'black'),
                    horizontalalignment = 'left', verticalalignment = 'top')
        pass
    ax.set_xlim(['1/1/2007', '1/1/2011'])
    ax.set_ylim([600, 1800])
    ax.set_title("Important dates in 2008-2009 financial crisis")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # 绘图
    rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color = 'k', alpha = 0.3)
    circ = plt.Circle((0.7, 0.2), 0.15, color = 'b', alpha = 0.3)
    pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]], color = 'g',
                       alpha = 0.5)

    ax.add_patch(rect)
    ax.add_patch(circ)
    ax.add_patch(pgon)


# ch080105. 将图表保存到文件
def ch080105_savefig():
    # P244，表8-2：Figure.savefig 的参数
    # 1. fname：含有文件路径的字符串或者 Python 的文件型对象。图像匝文件扩展名推断得出
    # 2. dpi：图像分辨率（每英寸点数），默认（100）
    # 3. facecolor, edgecolor：图像的背景色，默认（白）
    # 4. format：显式设置文件格式
    # 5. bbox_inches：图表需要保存的部分。'tight'：尝试剪除图表周围的空白部分
    from io import StringIO

    plt.savefig('figpath.svg')
    plt.savefig('figpath.png', dpi = 400, bbox_inches = 'tight')
    buffer = StringIO()  # 文件型对象
    plt.savefig(buffer)  # 写入任何文件型对象
    plot_data = buffer.getvalue()


# ch080105. matplotlib 配置
plt.rc('figure', figsize = (10, 100))  # 直接根据关键字设置
font_options = {'family': 'monospace', 'weight': 'bold', 'size': 'small'}
plt.rc('font', **font_options)  # 利用字典设置
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
