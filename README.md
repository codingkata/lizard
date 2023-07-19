
## 生成 C5, C10, C15, C20, C25 和 C30 的千行代码圈复杂度超标率，并写入一个csv文件


```
$ python3 cc.py -l java -x "**/test/*" -I 5 -B master -o output.csv <the local folder for your repo>
```

生成的文件格式如下：

```
time,rev,nloc,C5,C10,C15,C20,C25,C30
2013-12-12 21:26:17,cfe900930d92fc0372442f4b18dd81003d2cfd78,62036,58.51,30.93,20.04,13.69,9.16,5.61
2014-06-03 17:46:17,320c6465e49f53e85f12cd96ec8da1f354dad7c0,105270,44.37,21.88,13.94,9.58,6.47,4.02
2014-07-10 15:14:47,aeccbaab4e2623c86bb5910ed54bfc3ea2985f9a,105289,44.35,21.87,13.93,9.57,6.47,4.02
2014-07-25 13:45:36,5d865813291eb6f215becee10b3f14193b59f2ad,105298,44.34,21.87,13.93,9.57,6.47,4.02
2014-09-02 12:00:38,34a24d0044516fc31a7ae6500ac22d09c508717c,105390,44.29,21.85,13.92,9.56,6.46,4.01
```

## 用圈复杂度超标率时间轴文件，生成一个图片


```
$ python3 cctocurve.py <your outputfile> <time interval>
```

注意：确保输入文件格式如上面所示，输出为当前目录下的 一个 PNG 文件，它的 basename 与输入文件相同。


## 生成一个圈复杂度与函数个数的反比例曲线图片


```
$ python3 cc.py -l java -x "**/test/*" --skewed <the local folder for your repo>
```

输出的文件名为： cc_distribution.png


