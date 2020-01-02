# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch0705_USDA.py
@Version    :   v0.1
@Time       :   2019-12-24 16:38
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec0705，P224
@Desc       :   数据规整化：清理、转换、合并、重塑，示例：USDA食品数据库
@理解：
"""
import json
from pprint import pprint as pp

import matplotlib.pyplot as plt
import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import DataFrame

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 8, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
db = json.load(open('ch07/foods-2011-10-03.json'))
print(len(db))
print(db[0].keys())

nutrients = DataFrame(db[0]['nutrients'])
print(nutrients[:7])

info_keys = ['description', 'group', 'id', 'manufacturer']
info = DataFrame(db, columns = info_keys)
print(info[:5])
print(info.head())
print(pd.value_counts(info.group))

nutrients = []
for rec in db:
    fnuts = DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
    pass
nutrients = pd.concat(nutrients, ignore_index = True)
pp(nutrients)
pp(nutrients.duplicated().sum())

nutrients = nutrients.drop_duplicates()
col_mapping = {'description': 'food', 'group': 'fgroup'}
info = info.rename(columns = col_mapping, copy = False)
pp(info)

col_mapping = {'description': 'nutrient', 'group': 'nutgroup'}
nutrients = nutrients.rename(columns = col_mapping, copy = False)
pp(nutrients)

ndata = pd.merge(nutrients, info, on = 'id', how = 'outer')
pp(ndata.loc[30000])

result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
result['Zinc, Zn'].sort_values().plot(kind = 'barh')
by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])
get_maximum = lambda x: x.xs(x.value.idxmax())
max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]

max_foods.loc['Amino Acids', 'Alanine']['food']
# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
if len(plt.get_fignums()) != 0:
    plt.show()
pass
