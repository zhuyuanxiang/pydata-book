# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch02_movie_lens.py
@Version    :   v0.1
@Time       :   2019-12-10 18:20
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0202，P29
@Desc       :   介绍一些例子，MovieLens 1M 数据集
@理解：
"""
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
import winsound

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位

np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']

show_title("用户数据集中的前五个")
users = pd.read_table('movielens/users.dat', sep = '::', header = None,
                      names = unames)
print(users[:5])

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
show_title("排名数据集中的前五个")
ratings = pd.read_table('movielens/ratings.dat', sep = '::', header = None,
                        names = rnames)
print(ratings[:5])

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('movielens/movies.dat', sep = '::', header = None,
                       names = mnames)
show_title("电影数据集中的前五个")
print(movies[:5])

show_title("完整数据集中的前五个")
data = pd.merge(pd.merge(ratings, users), movies)
print(data[:5])

show_title("按“性别（gender）”计算每部电影的平均得分的前五个")
mean_ratings = data.pivot_table(values = ['rating'], index = ['title'],
                                columns = 'gender', aggfunc = 'mean')
print(mean_ratings[:5])

show_title("按“标题（title）”分组的结果数据集的前五个")
ratings_by_title = data.groupby('title').size()
print(ratings_by_title[:5])

active_titles = ratings_by_title.index[ratings_by_title >= 250]
show_title("评分数据超过250条的电影数据集的前五个")
print(active_titles[:5])

# .ix 已经废弃的属性
# mean_ratings = mean_ratings.ix[active_titles]
show_title("按“性别（gender）”计算超过250条数据的每部电影的平均得分的前五个")
mean_ratings = mean_ratings.loc[active_titles]
print(mean_ratings[:5])

# .sort_index()已经被废弃
# top_female_ratings = mean_ratings.sort_index(by='F', ascending = False)
show_title("按女性的平均得分排序的前五个")
top_female_ratings = mean_ratings.sort_values(by = [('rating', 'F')],
                                              ascending = False)
print(top_female_ratings[:5])

# 增加一个新的列，用于存放平均得分之差（男性评价 - 女性评价）
show_title("增加了平均得分之差列的数据集的前五个")
mean_ratings[('rating', 'diff')] = mean_ratings[('rating', 'M')] - mean_ratings[
    ('rating', 'F')]
print(mean_ratings[:5])

show_title("对平均得分之差按照升序排列后的数据集的前五个")
sorted_by_diff = mean_ratings.sort_values(by = ('rating', 'diff'))
print(sorted_by_diff[:5])
print("对平均得分之差按照升序排列后的数据集的后五个")
print(sorted_by_diff[-5:])
print("对平均得分之差按照降序排列后的数据集的后五个")
print(sorted_by_diff[::-1][:5])

show_title("根据电影名称分组的得分数据的标准差的数据集的前五个")
rating_std_by_title = data.groupby('title')['rating'].std()
print(rating_std_by_title[:5])

show_title("根据电影名称分组的得分数据的标准差的数据集经过active_titles（超过250条数据）过滤后的数据集的前五个")
rating_std_by_title = rating_std_by_title.loc[active_titles]
print(rating_std_by_title[:5])

# .order() 函数不存在，ToSee：为什么没有声明为废弃呢？
# print(rating_std_by_title.order(ascending = False)[:5])
show_title("排序后的数据集的前五个")
print(rating_std_by_title.sort_values(ascending = False)[:5])

# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
