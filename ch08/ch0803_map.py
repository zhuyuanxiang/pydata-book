# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0803_map.py
@Version    :   v0.1
@Time       :   2019-12-25 9:43
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0803，P254
@Desc       :   绘图和可视化，绘制地图：图形化显示海地地震数据
@理解：不太喜欢这个案例，就不重做了
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
data = pd.read_csv('Haiti.csv')
show_title("原始数据的列名称")
pp(data.columns)
show_title("每条数据表示从某人的手机上发送的紧急或者其他问题的报告")
pp(data.head())
show_title("每条报告都有一个时间戳和位置（经度和纬度）")
pp(data[['INCIDENT DATE', 'LATITUDE', 'LONGITUDE']].head())
show_title("每条报告都有消息的类型，使用逗号分隔的代码描述")
pp(data['CATEGORY'].head())
show_title("数据的统计信息")
pp(data.describe())
show_title("消除错误的位置信息+移除缺失分类的信息")
data = data[
    (data.LATITUDE > 18) & (data.LATITUDE < 20) & (data.LONGITUDE > -75) & (
                data.LONGITUDE < -70) & data.CATEGORY.notnull()]
pp(data.head())


# 获取所有分类的列表
def to_cat_list(catstr):
    stripped = (x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]


def get_all_categories(cat_series):
    cat_sets = (set(to_cat_list(x)) for x in cat_series)
    return sorted(set.union(*cat_sets))


# 将各个分类信息拆分为编码和英语名称
def get_english(cat):
    code, names = cat.split('.')
    if '|' in names:
        names = names.split('|')[1]
        pass
    return code, names.strip()


# 测试函数
get_english('2. Urgences logistiques | Vital Lines')

all_cats = get_all_categories(data.CATEGORY)
print(data.CATEGORY)
print(all_cats)
english_mapping = dict(get_english(x) for x in all_cats)
pp(english_mapping)
print(english_mapping['2a'])
print(english_mapping['6c'])


def get_code(seq):
    return [x.split('.')[0] for x in seq if x]


all_codes = get_code(all_cats)
code_index = pd.Index(np.unique(all_codes))
dummy_frame = DataFrame(np.zeros((len(data), len(code_index))),
                        index = data.index, columns = code_index)
pp(dummy_frame.iloc[:, :6])

for row, cat in zip(data.index, data.CATEGORY):
    codes = get_code(to_cat_list(cat))
    dummy_frame.ix[row, codes] = 1
    pass
data = data.join(dummy_frame.add_prefix('category_'))
print(data.ix[:, 10:15])

from mpl_toolkits.basemap import Basemap


def basic_haiti_map(ax = None, lllat = 17.25, urlat = 20.25, lllon = -75,
                    urlon = -71):
    # 创建极球面投影的Basemap实例
    m = Basemap(ax = ax, projection = 'stere', lon_0 = (urlon + lllon) / 2,
                lat_0 = (urlat + lllat) / 2, llcrnrlat = lllat,
                urcrnrlat = urlat, llcrnrlon = lllon, urcrnrlon = urlon,
                resolution = 'f')
    # 绘制海岸线、州界、国界以及地图边界
    m.drawcoastlines()
    m.drawstates()
    m.drawcounties()
    return m


fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (12, 10))
fig.subplots_adjust(hspace = 0.05, wspace = 0.05)
to_plot = ['2a', '1', '3c', '7a']
lllat, urlat = 17.25, 20.25
lllon, urlon = -75, -71
for code, ax in zip(to_plot, axes.flat):
    m = basic_haiti_map(ax, lllat = lllat, urlat = urlat, lllon = lllon,
                        urlon = urlon)
    cat_data = data[data['category_{}'.format(code)] == 1]

    # 计算地图的投影坐标
    x, y = m(cat_data.LONGITUDE, cat_data.LATITUDE)
    m.plot(x, y, 'k.', alpha = 0.5)
    ax.set_title('{}: {}'.format(code, english_mapping[code]))
    pass

shapefile_path = 'PortAuPrince_Roads/PortAuPrince_Roads'
m.readshapefile(shapefile_path, 'roads')

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
