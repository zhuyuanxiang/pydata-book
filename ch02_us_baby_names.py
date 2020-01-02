# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch02_us_baby_names.py
@Version    :   v0.1
@Time       :   2019-12-11 10:29
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec02003，P35
@Desc       :   介绍一些例子，1880-2010年间全美婴儿姓名
@理解：
"""
# common imports

from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
import winsound

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样

# ----------------------------------------------------------------------
show_title("1880年美国出生婴儿名称数据集前五个")
names1880 = pd.read_csv('ch02/names/yob1880.txt',
                        names = ['name', 'sex', 'births'])
print(names1880[:5])

show_title("数据集按性别分组，按照出生人数统计")
print(names1880.groupby('sex').births.sum())

years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = 'ch02/names/yob{}.txt'.format(year)
    frame = pd.read_csv(path, names = columns)
    frame['year'] = year
    pieces.append(frame)
    pass
# 将所有的数据整合到单个的DataFrame中
# 1. concat()默认是按行将多个 DataFrame组合到一起
# 2. ignore_index=True，避免保留read_csv()返回的原始行号
show_title("组合的数据集的前五个")
names = pd.concat(pieces, ignore_index = True)
print(names[:5])

show_title("对数据集针对year和sex字段进行聚合")
total_births = names.pivot_table(values = 'births', index = 'year',
                                 columns = 'sex', aggfunc = 'sum')
print(total_births.tail())
total_births.plot(title = "按性别和年度统计的总出生数")


def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group


show_title("对数据集针对year和sex字段进行分组")
names = names.groupby(['year', 'sex']).apply(add_prop)
print(names.tail())

show_title("使用allclose()函数测试分组prop字段总计值是否接近于1")
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)


def get_top1000(group):
    # ToKnown:这里是先取数据再排序
    return group.sort_values(by = 'births', ascending = False)[:1000]


show_title("将数据按照year和sex字段分组，再基于每个分组取出1000条数据，然后基于births字段进行排序")
# groupby() 只是将数据分组，并没有统计，分组里面存储的是数组的序号
grouped = names.groupby(['year', 'sex'])
top1000 = names.groupby(['year', 'sex']).apply(get_top1000)
print(top1000[:20])
print(len(top1000))

show_title("分析命名趋势")
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
total_births = names.pivot_table(values = 'births', index = 'year',
                                 columns = 'name', aggfunc = 'sum')
print(total_births.tail())
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots = True, figsize = (12, 10), grid = False,
            title = "图2-5：男孩和女孩名字使用数量随时间变化的趋势")

show_title("评估命名多样性的增长")
table = names.pivot_table(values = 'prop', index = 'year', columns = 'sex',
                          aggfunc = 'sum')
table.plot(title = "按照性别统计在总出生人数中的比例", yticks = np.linspace(0, 1.2, 13),
           xticks = range(1880, 2020, 10))

df = boys[boys.year == 2010]
show_title("df")
pp(df)

# .sort_index()已经被废弃
prop_cumsum = df.sort_values(by = 'prop', ascending = False).prop.cumsum()
show_title("prop_cumsum")
pp(prop_cumsum.head())
print("prop_cumsum.searchsorted(0.5) =", prop_cumsum.searchsorted(0.5))

df = boys[boys.year == 1900]
in1900 = df.sort_values(by = 'prop', ascending = False).prop.cumsum()
print("prop_cumsum.searchsorted(0.5) =", prop_cumsum.searchsorted(0.5) + 1)


def get_quantile_count(group, q = 0.5):
    group = group.sort_values(by = 'prop', ascending = False)
    return group.prop.cumsum().searchsorted(q) + 1


diversity = names.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
show_title("diversity")
pp(diversity.head())

diversity.plot(title = "图2-7：按年度统计的密度表")

show_title("最后一个字母的变化")
last_letters = names.name.map(lambda x: x[-1])
last_letters.name = 'last_letter'
table = names.pivot_table('births', index = last_letters,
                          columns = ['sex', 'year'], aggfunc = sum)
subtable = table.reindex(columns = [1910, 1960, 2010], level = 'year')
show_title("选出有代表性的数据")
pp(subtable)
show_title("subtable.sum()")
pp(subtable.sum())
letter_prop = subtable / subtable.sum().astype(float)

fig, axes = plt.subplots(2, 1, figsize = (10, 8))
letter_prop['M'].plot(kind = 'bar', rot = 0, ax = axes[0], title = '男')
letter_prop['F'].plot(kind = 'bar', rot = 0, ax = axes[1], title = '女',
                      legend = False)

letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
show_title("dny_ts")
pp(dny_ts.head())
dny_ts.plot(title = "图2-9：不同年份中的出生的男孩的名字以d/n/y结尾的人数比例")

all_names = names.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
show_title("以 'lesl' 开头的一组名字")
pp(lesley_like)

filterd = names[names.name.isin(lesley_like)]
show_title("统计以 'lesl' 开头的一组名字的人数")
filterd.groupby('name').births.sum()

table = filterd.pivot_table('births', index = 'year', columns = 'sex',
                            aggfunc = sum)
table = table.div(table.sum(1), axis = 0)
show_title("按性别和年度进行聚合得到的最后几年的数据")
pp(table.tail())
table.plot(style = {'M': 'k-', 'F': 'k--'},
           title = "图2-10：各年度使用“Lesley型”名字的男女比例")

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
plt.show()
