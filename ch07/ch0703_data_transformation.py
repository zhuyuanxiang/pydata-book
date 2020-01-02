# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0703_data_transformation.py
@Version    :   v0.1
@Time       :   2019-12-22 17:28
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0703，P204
@Desc       :   数据规整化：清理、转换、合并、重塑，数据转换
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
# common imports
import pandas as pd
import winsound
from pandas import DataFrame, Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 119)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样


# ----------------------------------------------------------------------
# ch070301. 移除重复数据
def ch070301_duplicate():
    data = DataFrame({
            'k1': ['one'] * 4 + ['two'] * 4, 'k2': [1, 1, 2, 3, 3, 4, 4, 4]
    })
    show_title("原始数据")
    pp(data)
    show_title("检查数据中是否存在重复的行数据")
    pp(data.duplicated())
    show_title("删除数据中存在重复的行数据")
    pp(data.drop_duplicates())

    data['v1'] = range(8)
    show_title("原始数据")
    pp(data)
    show_title("删除数据中指定列存在重复的行数据，默认保留第一个数据")
    pp(data.drop_duplicates(['k1']))
    show_title("删除数据中指定列存在重复的行数据，指定保留最后一个数据")
    pp(data.drop_duplicates(['k1'], keep = 'last'))


# ch070302. 利用函数或者映射进行数据转换
def ch070302_mapping():
    data = DataFrame({
            'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami', 'corned beef',
                     'Bacon', 'pastrami', 'honey ham', 'nova lox'],
            'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]
    })
    show_title("原始数据")
    pp(data)
    meat_to_animal = {
            'bacon': 'pig', 'pulled pork': 'pig', 'pastrami': 'cow',
            'corned beef': 'cow', 'honey ham': 'pig', 'nova lox': 'salmon'
    }
    data['animal'] = data['food'].map(str.lower).map(meat_to_animal)
    show_title("映射后的数据")
    pp(data)

    data['animal_lambda'] = data['food'].map(
        lambda x: meat_to_animal[x.lower()])
    show_title("lambda 映射后的数据")
    pp(data)


# ch070303.替换值
def ch070303_replace():
    data = Series([1., -999., 2., -999., -1000., 3.])
    show_title("原始数据")
    pp(data)
    show_title("替换后的数据")
    pp(data.replace(-999, np.nan))
    show_title("替换批量值后的数据")
    pp(data.replace([-999, -1000], np.nan))
    show_title("批量替换值后的数据")
    pp(data.replace([-999, -1000], [np.nan, 0]))
    show_title("基于字典批量替换值后的数据")
    pp(data.replace({-999: np.nan, -1000: 0}))


# ch070304.重命名轴索引
def ch070304_rename():
    data = DataFrame(np.arange(12).reshape((3, 4)),
                     index = ['Ohio', 'Colorado', 'New York'],
                     columns = ['one', 'two', 'three', 'four'])
    show_title("原始数据")
    pp(data)
    data.index = data.index.map(str.upper)
    show_title("使用映射重命名轴索引后的数据")
    pp(data)
    show_title("使用rename重命名轴索引创建新数据集")
    pp(data.rename(index = str.title, columns = str.upper))
    show_title("使用rename结合字典重命名轴索引创建新数据集")
    pp(data.rename(index = {'OHIO': 'INDIANA'},
                   columns = {'three': 'peekaboo'}))
    show_title("使用rename结合字典重命名轴索引修改原数据集")
    pp(data.rename(index = {'OHIO': 'INDIANA'}, inplace = True))
    pp(data)


# ch070305.离散化和分箱化
def ch070305_discretization():
    ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
    bins = [18, 25, 35, 60, 100]
    cats = pd.cut(ages, bins)
    show_title("原始数据")
    pp(cats)
    pp(cats.categories)
    pp(cats.codes)
    pp(pd.value_counts(cats))

    ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
    bins = [18, 26, 36, 61, 100]
    cats = pd.cut(ages, bins)
    show_title("原始数据分箱")
    pp(cats)
    cats = pd.cut(ages, bins, right = False)
    show_title("使用开区间分箱")
    pp(cats)
    group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
    cats = pd.cut(ages, bins, labels = group_names)
    show_title("设置箱子的名称")
    pp(cats)

    data = np.random.rand(20)
    show_title("原始数据")
    pp(cats)
    cats = pd.cut(data, 4, precision = 2)
    show_title("根据数据的最小值和最大值计算等长箱宽")
    pp(cats)

    data = np.random.randn(1000)
    cats = pd.qcut(data, 4)
    show_title("按四分位数进行切割")
    pp(cats)
    show_title("统计箱子中的数目")
    pp(pd.value_counts(cats))
    cats = pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.])
    show_title("设置自定义的分位数")
    pp(cats)
    show_title("统计箱子中的数目")
    pp(pd.value_counts(cats).sort_index())


# ch070306. 检测和过滤异常值
def ch070306_outliers():
    data = DataFrame(np.random.randn(1000, 4))
    show_title("数据的统计指标")
    pp(data.describe())
    show_title("第4列中绝对值大于3的值")
    pp(data[3][np.abs(data[3]) > 3])
    show_title("行数据中含有绝对值大于3的值")
    pp(data[(np.abs(data) > 3).any(1)])
    data[np.abs(data) > 3] = np.sign(data) * 3
    show_title("替换所有绝对值大于3的数据为对应正负号的3，关注最大值和最小值")
    pp(data.describe())


# ch070307. 排列和随机采样
def ch070307_random_sample():
    show_title("随机排列矩阵")
    sampler = np.random.permutation(5)
    pp(sampler)
    show_title("原始数据")
    df = DataFrame(np.arange(5 * 4).reshape(5, 4))
    pp(df)
    show_title("随机排列后的数据")
    pp(df.take(sampler))
    show_title("permutation()随机采样后得到的数据")
    pp(df.take(np.random.permutation(len(df))[:3]))
    show_title("randint()随机采样后得到的数据")
    pp(df.take(np.random.randint(0, len(df), size = 10)))
    show_title("randint()对一维数据随机采样后得到的数据")  # ToKnown：更容易理解
    bag = np.array([5, 7, -1, 6, 4])
    pp(bag.take(np.random.randint(0, len(bag), size = 10)))


# ch070308. 计算指标/哑变量
df = DataFrame({
        'key': ['b', 'b', 'a', 'c', 'a', 'b'],
        'data1': np.random.randint(0, 10, size = 6)
})
show_title("原始数据")
pp(df)
show_title("将分类变量转换为“哑变量矩阵”或者“指标矩阵”")  # 等价于One-Hot编码
pp(pd.get_dummies(df['key']))

dummies = pd.get_dummies(df['key'], prefix = 'key')
df_with_dummy = df[['data1']].join(dummies)
show_title("原始数据和指标矩阵合并")
pp(df_with_dummy)

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('../ch02/movielens/users.dat', sep = '::', header = None,
                      names = unames)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('../ch02/movielens/ratings.dat', sep = '::',
                        header = None, names = rnames)
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('ch02/movielens/movies.dat', sep = '::', header = None,
                       names = mnames, engine = 'python')
genre_iter = (set(x.split('|')) for x in movies.genres)
genres = sorted(set.union(*genre_iter))
dummies = DataFrame(np.zeros((len(movies), len(genres))), columns = genres)
for i, gen in enumerate(movies.genres):
    dummies.loc[i, gen.split('|')] = 1
    pass
movies_windic = movies.join(dummies.add_prefix('Genre_'))
pp(movies_windic.loc[0])

values = np.random.rand(10)
pp(values)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
pp(pd.get_dummies(pd.cut(values, bins)))

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
