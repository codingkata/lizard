import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os

"""
<output_file> 是由下面的命令生成。

$ python3 cc.py -l java -x "**/test/*" -I 200 -B master -o <output_file> <the local folder of your git repo>

输入：

-I: 每隔 200个 commit 计算一次
-B: 分支名为 master
-x: 排除这个格式的文件
-l: 编程语言

输出格式如下：
time,rev,nloc,C5,C10,C15,C20,C25,C30
2013-12-12 21:26:17,cfe900930d92fc0372442f4b18dd81003d2cfd78,62036,58.51,30.93,20.04,13.69,9.16,5.61
2014-06-03 17:46:17,320c6465e49f53e85f12cd96ec8da1f354dad7c0,105270,44.37,21.88,13.94,9.58,6.47,4.02
2014-07-10 15:14:47,aeccbaab4e2623c86bb5910ed54bfc3ea2985f9a,105289,44.35,21.87,13.93,9.57,6.47,4.02
2014-07-25 13:45:36,5d865813291eb6f215becee10b3f14193b59f2ad,105298,44.34,21.87,13.93,9.57,6.47,4.02
2014-09-02 12:00:38,34a24d0044516fc31a7ae6500ac22d09c508717c,105390,44.29,21.85,13.92,9.56,6.46,4.01

"""

if len(sys.argv) < 3:
    print("Usage: python3 cctocurve.py <input_file> <interval>")
    print("The output is a png file with same name of <input_file>.")
    sys.exit(-1)

input_file = sys.argv[1]
interval = int(sys.argv[2])

df = pd.read_csv(input_file, parse_dates=['time'], date_parser=pd.to_datetime)

# 转换时间列为datetime格式
df['time'] = pd.to_datetime(df['time'])

# 绘制图像,设置为 10 x 6 英寸
plt.figure(figsize=(10, 6))

plt.plot(df['time'], df['C5'], label='C5')
plt.plot(df['time'], df['C10'], label='C10')
plt.plot(df['time'], df['C15'], label='C15')
plt.plot(df['time'], df['C20'], label='C20')
plt.plot(df['time'], df['C25'], label='C25')
plt.plot(df['time'], df['C30'], label='C30')
# 设置时间轴格式


ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))

plt.xlabel('time')
plt.ylabel('值')
plt.legend()
plt.gcf().autofmt_xdate()

outputfile = os.path.basename(input_file.split(".")[0]) + ".png"
# 设置dpi来控制图像质量,一般100-300 dpi就足够了
plt.savefig(outputfile, dpi=300)