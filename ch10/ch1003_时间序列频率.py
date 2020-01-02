# -*- encoding: utf-8 -*-    
"""
@Author     :   zYx.Tom
@Contact    :   526614962@qq.com
@site       :   https://zhuyuanxiang.github.io
---------------------------
@Software   :   PyCharm
@Project    :   pydata-book
@File       :   ch1003_时间序列频率.py
@Version    :   v0.1
@Time       :   2019-12-28 15:52
@License    :   (C)Copyright 2018-2019, zYx.Tom
@Reference  :   《利用 Python 进行数据分析，Wes McKinney》, Sec1003，P311
@Desc       :   时间序列，日期的范围、频率以及移动
@理解
"""
from datetime import datetime
from pprint import pprint as pp

import numpy as np  # pip install numpy<1.17，小于1.17就不会报错
import pandas as pd
# common imports
import winsound
from pandas import Series

from tools import show_title

# 设置数据显示的精确度为小数点后 4 位
np.set_printoptions(precision = 4, suppress = True, threshold = np.inf,
                    linewidth = 200)
np.random.seed(42)  # 利用随机种子，保证随机数据的稳定性，使得每次随机测试的结果一样
# ----------------------------------------------------------------------
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
         datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12), ]
time_series = Series(np.random.randn(6), index = dates)
show_title("time_series")
pp(time_series)
show_title("time_series.resample('D')")
resample = time_series.resample('D')
print(time_series.resample('D').obj)


def ch100301_日期的范围():
    show_title("pd.date_range('4/1/2012', '6/1/2012')")
    index = pd.date_range('4/1/2012', '6/1/2012')
    pp(index)

    show_title("pd.date_range(start='4/1/2012',periods=20)")
    pp(pd.date_range(start = '4/1/2012', periods = 20))

    show_title("pd.date_range(end='6/1/2012',periods=20)")
    pp(pd.date_range(end = '6/1/2012', periods = 20))

    show_title("pd.date_range('5/2/2012 12:56:31', periods = 5)")
    pp(pd.date_range('5/2/2012 12:56:31', periods = 5))
    pp(pd.date_range('5/2/2012 12:56:31', periods = 5, normalize = True))


def ch100302_日期的偏移量():
    # P314，表10-4：时间序列的基础频率(freq)
    # 1. D，Day：每个日历日
    # 2. B，BusinessDay：每个工作日
    # 3. H，Hour：每个小时
    # 4. T或min，Minute：每个分钟
    # 5. S，Second：每一秒
    # 6. L或ms，Milli：每一毫秒（千分之一秒）
    # 7. U，Micro：每一微秒（百分分之一秒）
    # 10. MS：MonthBegin：每月第一个日历日
    # 8. M，MonthEnd：每月最后一个日历日
    # 11. BMS：BusinessMonthBegin：每月第一个工作日
    # 9. BM：BusinessMonthEnd：每月最后一个工作日
    # 12. W-MON、W-TUE...，Week：从指定的星期几（MON、TUE、WEB、THU、FRI、SAT、SUN）开始算起每个周
    # 13. WOM-1MON、WOM-2MON...，WeekOfMonth：产生每月第一、第二、第三或者第四周的星期几。例如：WOM-3FRI表示每月第三个星期五
    # 16. QS-JAN、QS-FEB...，QuarterBegin：对于以指定月份结束的年度，每个季度最后一月的第一个日历日
    # 14. Q-JAN、Q-FEB...，QuarterEnd：对于以指定月份结束的年度，每个季度最后一个月的最后一个日历日
    # 17. BQS-JAN、BQS-FEB...，BusinessQuarterBegin：对于以指定月份结束的年度，每个季度最后一月的第一个工作日
    # 15. BQ-JAN、BQ-FEB...，BusinessQuarterEnd：对于以指定月份结束的年度，每个季度最后一月的最后一个工作日
    # 20. AS-JAN、AS-FEB...，YearBegin：每年指定月份的第一个日历日
    # 18. A-JAN、A-FEB...，YearEnd：每年指定月份的最后一个日历日
    # 21. BAS-JAN、BAS-FEB...，BusinessYearBegin：每年指定月份的第一个工作日
    # 19. BA-JAN、BA-FEB...，BusinessYearEnd：每年指定月份的最后一个工作日
    from pandas.tseries.offsets import Hour, Minute

    hour = Hour()
    show_title("hour")
    pp(hour)

    four_hours = Hour(4)
    show_title("Hour(4)")
    pp(four_hours)

    show_title("每'4个小时'作为间隔的时间序列索引")
    pp(pd.date_range('1/1/2000', '1/3/2000 23:59', freq = '4h'))

    show_title("Hour(2)+Minute(30)")
    pp(Hour(2) + Minute(30))

    show_title("每'1个小时30分钟'作为间隔的时间序列索引")
    pp(pd.date_range('1/1/2000', periods = 10, freq = '1h30min'))


def ch10030201_WOM日期():
    # WOM(Week Of Month)
    rng = pd.date_range('1/1/2000', '9/1/2012', freq = 'WOM-3FRI')
    show_title("每月第三个星期五作为频率")
    pp(list(rng)[:10])


def ch100303_移动数据():
    time_series = Series(np.random.randn(4),
                         index = pd.date_range('1/1/2000', periods = 4,
                                               freq = 'M'))
    show_title("time_series")
    pp(time_series)
    show_title("time_series.shift(2)")
    pp(time_series.shift(2))
    show_title("time_series.shift(-2)")
    pp(time_series.shift(-2))

    show_title("时间序列的变化百分比")
    pp(time_series / time_series.shift(1) - 1)

    show_title("time_series")
    pp(time_series)
    show_title("time_series.shift(2, freq = 'M')")
    pp(time_series.shift(2, freq = 'M'))
    show_title("time_series.shift(3, freq = 'D')")
    pp(time_series.shift(3, freq = 'D'))
    show_title("time_series.shift(1, freq = '3D')")
    pp(time_series.shift(1, freq = '3D'))
    show_title("time_series.shift(1, freq = '90T')")
    pp(time_series.shift(1, freq = '90T'))


def ch10030301_偏移量位移():
    from pandas.tseries.offsets import Day, MonthEnd

    now = datetime(2011, 11, 17)
    print("now =", now)
    print("now + 3 * Day() =", now + 3 * Day())
    print("now + MonthEnd() =", now + MonthEnd())
    print("now + MonthEnd(2) =", now + MonthEnd(2))

    offset = MonthEnd()
    print("now =", now)
    print("offset.rollforward(now) =", offset.rollforward(now))
    print("offset.rollback(now) =", offset.rollback(now))

    time_series = Series(np.random.randn(20),
                         index = pd.date_range('1/1/2000', periods = 20,
                                               freq = '4d'))
    show_title("time_series")
    pp(time_series)
    show_title("time_series.groupby(offset.rollforward).mean()")
    pp(time_series.groupby(offset.rollforward).mean())
    show_title("time_series.resample('M', how = 'mean')")
    pp(time_series.resample('M', how = 'mean'))
    pp(time_series.resample('M').mean())


# ----------------------------------------------------------------------
# 运行结束的提醒
winsound.Beep(600, 500)
