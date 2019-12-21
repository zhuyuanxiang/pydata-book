# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0604_database.py
@Version    :   v0.1
@Time       :   2019-12-20 18:57
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0604，P182
@Desc       :   数据加载、存储与文件格式，使用数据库
@理解：
"""
from pprint import pprint as pp

import matplotlib.pyplot as plt
# common imports
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import winsound
from pandas import DataFrame

# 设置数据显示的精确度为小数点后3位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf, linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
import sqlite3

query = """
CREATE TABLE test
(a VARCHAR(20),b VARCHAR(20), c REAL, d INTEGER);
"""
con = sqlite3.connect(':memory:')
con.execute(query)
con.commit()

data = [('Atlanta', 'Georgia', 1.25, 6), ('Tallahassee', 'Florida', 2.6, 3), ('Sacramento', 'California', 1.7, 5)]
stmt = "INSERT INTO test VALUES(?,?,?,?)"
con.executemany(stmt, data)
con.commit()

cursor = con.execute('select * from test')
rows = cursor.fetchall()
pp(rows)
pp(cursor.description)

data = DataFrame(rows, columns = [col for col in zip(*cursor.description)][0])
pp(data)

import pandas.io.sql as sql

pp(sql.read_sql('select * from test', con = con))

# ToKnown：放弃 MongoDB 的修改，因为也需要从网络中导入数据

print('-' * 5, "", '-' * 5)
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
