# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0905_example.py
@Version    :   v0.1
@Time       :   2019-12-27 14:15
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0905，P291
@Desc       :   数据取聚合与分组运算，例子（2012联邦选举委员会数据库）
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
fec = pd.read_csv('P00000001-ALL.csv')
show_title("原始数据")
pp(fec)
pp(fec.loc[123456])

unique_cands = fec.cand_nm.unique()
show_title("获取党派的信息")
pp(unique_cands)
pp(unique_cands[2])

parties = {
        'Bachmann, Michelle': 'Republican', 'Cain, Herman': 'Republican',
        'Gingrich, Newt': 'Republican', 'Huntsman, Jon': 'Republican',
        'Johnson, Gary Earl': 'Republican',
        'McCotter, Thaddeus G': 'Republican', 'Obama, Barack': 'Democrat',
        'Paul, Ron': 'Republican', 'Pawlenty, Timothy': 'Republican',
        'Perry, Rick': 'Republican',
        "Roemer, Charles E. 'Buddy' III": 'Republican',
        'Romney, Mitt': 'Republican', 'Santorum, Rick': 'Republican'
}
pp(fec.cand_nm[123456:123461])
pp(fec.cand_nm[123456:123461].map(parties))

# 添加一个党派列
fec['party'] = fec.cand_nm.map(parties)
# 党派数据的统计
pp(fec['party'].value_counts())
# 对赞助的统计
pp((fec.contb_receipt_amt > 0).value_counts())

fec = fec[fec.contb_receipt_amt > 0]
fec_子集 = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

# 根据职业和雇主统计赞助信息
show_title("根据职业计算出资总额")
pp(fec.contbr_occupation.value_counts().head())

occ_mapping = {
        'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
        'INFORMATION REQUESTED': 'NOT PROVIDED',
        'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED', 'C.E.O.': 'CEO'
}
# 如果没有提供相关映射，则返回 x
f = lambda x: occ_mapping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)

emp_mapping = {
        'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
        'INFORMATION REQUESTED': 'NOT PROVIDED', 'SELF': 'SELF-EMPLOYED',
        'SELF EMPLOYED': 'SELF-EMPLOYED'
}

# 如果没有提供相关映射，则返回 x
f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)

by_occupation = fec.pivot_table('contb_receipt_amt',
                                index = 'contbr_occupation', columns = 'party',
                                aggfunc = 'sum')
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
show_title("根据党派和职业对数据进行聚合，过滤总出资额不足200万美元的数据")
pp(over_2mm)

over_2mm.plot(kind = 'barh')
plt.title("图9-2：对各党派总出资额最高的职业")


def get_top_amounts(group, key, n = 5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    # 根据 key 对 totals 进行降序排列
    return totals.sort_index(ascending = False)[:n]


grouped = fec_子集.groupby('cand_nm')
show_title("根据职业进行聚合")
pp(grouped.apply(get_top_amounts, 'contbr_occupation', n = 7))
show_title("根据雇主进行聚合")
pp(grouped.apply(get_top_amounts, 'contbr_employer', n = 10))

# 对出资额分组
bins = np.array([0, 1, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7])
labels = pd.cut(fec_子集.contb_receipt_amt, bins)
show_title("利用 cut 函数根据出资额的大小将数据离散化到多个箱子中")
pp(labels)

grouped = fec_子集.groupby(['cand_nm', labels])
show_title("根据候选人姓名以及箱子的标签对数据进行分组")
pp(grouped.size().unstack(0))

bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
show_title("对出资额求和")
pp(bucket_sums)

normed_sums = bucket_sums.div(bucket_sums.sum(axis = 1), axis = 0)
show_title("在箱子内归一化")
pp(normed_sums)

normed_sums[:-2].plot(kind = 'barh', stacked = True)
plt.title("图9-3：两位候选人收到的各种捐赠额度的总额比例\n（排除了两个最大的额度的捐赠，因为不是个人捐赠）")
plt.show()

# 根据州统计赞助信息
grouped = fec_子集.groupby(['cand_nm', 'contbr_st'])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 1e5]
show_title("各州赞助额度统计")
pp(totals.head())

percent = totals.div(totals.sum(1), axis = 0)
show_title("各州赞助比例统计")
pp(percent.head())

# ToDo：放弃绘图，无法得到相应的工具包
# from pyshp import ShapeFile  # conda install pyshp
# import dbflib
# import shapefile
#
# obama = percent['Obama, Brack']
# fig = plt.figure(figsize = (12, 12))
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# lllat, urlat = 21, 53
# lllon, urlon = -118, -62
# m = Basemap(ax = ax, projection = 'stere', lon_0 = (urlon + lllon) / 2, lat_0 = (urlat + lllat) / 2,
#             llcrnrlat = lllat, urcrnrlat = urlat,
#             llcrnrlon = lllon, urcrnrlon = urlon, resolution = 'l')
# m.drawcoastlines()
# m.drawcoutries()
#
# shp = ShapeFile('../states/statesp020')
# dbf = dbflib.open('../states/statesp020')
#
# for npoly in range(shp.info()[0]):
#     # 在地图上绘制彩色多边形
#     shpsegs = []
#     shp_object = shp.read_object(npoly)
#     verts = shp_object.vertices()
#     rings = len(verts)
#     for ring in range(rings):
#         lons, lats = zip(*verts[ring])
#         x, y = m(lons, lats)
#         shpsegs.append(zip(x, y))
#         if ring == 0:
#             shapedict = dbf.read_object(npoly)
#             pass
#         name = shapedict['STATE']
#         pass
#     lines = LineCollection(shpsegs, antialiaseds = (1,))
#
#     # state_to_code 字典，例如：'ALASKA' -> 'AK'，omitted
#     try:
#         per = obama[state_to_code[name.upper()]]
#     except KeyError:
#         continue
#         pass
#
#     lines.set_facecolor('k')
#     lines.set_alpha(0.75 * per)  # 把“百分比”变小一点
#     lines.set_edgecolor('k')
#     lines.set_linewidth(0.3)
#     pass

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
