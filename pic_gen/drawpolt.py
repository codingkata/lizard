import matplotlib.pyplot as plt


def draw_skewed_curve(counts):
  # 按键排序
  sorted_counts = dict(sorted(counts.items()))
  x = []
  y = []
  for k, v in sorted_counts.items():
    print(k,v)
    x.append(k)
    y.append(v)

  # 绘制图像,设置为 10 x 6 英寸
  plt.figure(figsize=(10, 15))

  plt.plot(x, y)
  plt.xlabel('CC Number')
  plt.ylabel('Number of func')
  plt.title('cc_distribution')

  # 设置dpi来控制图像质量,一般100-300 dpi就足够了
  plt.savefig("cc_distribution.png", dpi=300)
