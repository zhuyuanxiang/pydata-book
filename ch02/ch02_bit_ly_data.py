# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch02_bit_ly_data.py
@Version    :   v0.1
@Time       :   2019-12-10 16:03
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0201，P20
@Desc       :   介绍一些例子，来自 bit.ly 的 1.usa.gov 的数据
@理解：
"""
# common imports
import json
from collections import Counter, defaultdict

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from pandas import DataFrame, Series

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样

# ----------------------------------------------------------------------
path = 'usagov_bitly_data2012-03-16-1331923249.txt'
print("使用 Python 内建函数读取数据：\n", open(path).readline())
print('-' * 50)
records = [json.loads(line) for line in open(path)]
print("使用 JSON 转换读取的数据--records[0]：\n", records[0])
print('-' * 50)
print("取出记录对应关键字的内容：records[0]['tz'] = ", records[0]['tz'])
print('-' * 50)
print("数据文件存在错误时，无法正确提取时区数据")
print("time_zones=[rec['tz'] for rec in records]")
# time_zones=[rec['tz'] for rec in records]

# 增加 if 条件判断就可以正确提取时区数据了
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
print('-' * 50)
print("输出统计时区的前十个结果：\n", time_zones[:10])


# 统计函数：统计数据中出现的某种数据的个数
# 使用 Python 标准库的简单实现
def get_counts_simple_python(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
            pass
        pass
    return counts


# 使用 Python 标准库的高级实现
def get_counts_advanced_python(sequence):
    counts = defaultdict(int)  # 所有的新出现的值都会自动初始化为0
    for x in sequence:
        counts[x] += 1
    return counts


time_zones_counts = get_counts_simple_python(time_zones)
print('-' * 50)
print("总共有多少条数据（已经过滤了错误数据，没有过滤空数据）：", len(time_zones))
print("总共有多少个时区：", len(time_zones_counts))
print("时区是America/New_York 的个数：", time_zones_counts['America/New_York'])


def top_counts(count_dict, n = 10):  # 默认取前10条数据
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()  # 升序排列
    return value_key_pairs[-n:]


print('-' * 50)
print("时区数据条数统计排名前十个：")
print(top_counts(time_zones_counts))

counts = Counter(time_zones)
print('-' * 50)
print("使用 Python 内建函数Counter()统计时区数据条数的排名前十个（没有排序）：\n", counts.most_common(10))

frame = DataFrame(records)
print('-' * 50)
print("看看Pandas的DataFrame是个啥？\n", frame)

print('-' * 50)
print("frame['tz'][:10] = ")
print(frame['tz'][:10])

tz_counts = frame['tz'].value_counts()
print('-' * 50)
print("使用 Pandas 的函数来进行统计（自动排序）：")
print(tz_counts[:10])

clean_tz = frame['tz'].fillna(
    'Missing')  # 将错误（NA）数据填充为 Missing，错误的就是没有 'tz' 字段的数据
clean_tz[clean_tz == ''] = 'Unknown'  # 将空数据填充为 Unknown
tz_counts = clean_tz.value_counts()
print('-' * 50)
print("使用 Pandas 的函数先填充再统计（自动排序）：")
print(tz_counts[:10])

# 绘制 统计数据的 直方图
# tz_counts[:10].plot(kind = 'barh', rot = 0)

print('-' * 50)
print("'a'字段中的数据：")
print(frame['a'])

results = Series(
        [x.split()[0] for x in frame.a.dropna()])  # 将 'a' 字段中的数据取出（不合法的数据放弃）
print('-' * 50)
print("将 'a' 字段中数据取出的效果")
print(results)

cframe = frame[frame.a.notnull()]
print('-' * 50)
print("将 'a' 字段中数据取出的效果")
print(cframe)

operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows',
                            'Not Windows')
print('-' * 50)
print("区分 'a' 字段中使用 'Windows' 的数据：")
print(operating_system[:5])

# groupby()： 对数据进行分组
# size()：对数据进行统计
# unstack()：将数据从字典转换成DataFrame格式
# fillna(0)：将不存在的数据填充为0，即统计结果为0
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print('-' * 50)
print("数据集中前十个使用Windows浏览器和不使用Windows浏览器的用户时区(按照时区的字母排序)")
print(agg_counts[:10])

# 对operating_system维度进行统计，然后再排序
indexer = agg_counts.sum(axis = 1).argsort()
print('-' * 50)
print("数据集中前十个用户时区统计结果排序位次(按照时区的字母排序)")
print(indexer[:10])

count_subset = agg_counts.take(indexer)[-10:]
print('-' * 50)
print("按照排序结果取得数据集的后十个数据：")
print(count_subset[-10:])

# 使用 stacked 可以绘制堆积条形图
# count_subset.plot(kind = 'barh', stacked = True)

# 将结果数据归一化，再绘制堆积条形图
normed_subset = count_subset.div(count_subset.sum(axis = 1), axis = 0)
normed_subset.plot(kind = 'barh', stacked = True)
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
