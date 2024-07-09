import matplotlib.pyplot as plt

# 数据：障碍物和目标位置
obstacles = [
    [3.645, 0.331000021457672, 4.42, 3.2040000476837154],
    [3.727694785714149, 3.6431662828922264, 4.464189401149749, 4.361847497403621],
    [3.727694785714149, 4.343166282892227, 4.464189401149749, 5.0618474974036225],
    [3.7081110202760694, 2.7691082409620287, 4.398934257864952, 3.6428384968042375],
    [3.73802099442482, 2.4950634858608245, 4.241272992730141, 3.2712760128974914],
    [3.186277736547578, 4.954778346326298, 4.409681093573571, 5.74132460463047],
    [3.936692001789808, 5.237203998237848, 4.063309000313282, 5.362882000088692]
]
goal = [3.0330712019698858, 5.548290838340196]

# 绘图
plt.figure(figsize=(10, 10))

# 绘制障碍物
for obs in obstacles:
    x_min, y_min, x_max, y_max = obs
    width = x_max - x_min
    height = y_max - y_min
    plt.gca().add_patch(plt.Rectangle((x_min, y_min), width, height, edgecolor='r', facecolor='none'))

# 绘制目标位置
plt.plot(goal[0], goal[1], 'bo', label='Goal')

plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.title('障碍物和目标位置')
plt.legend()
plt.grid(True)
plt.xlim(0, 6)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')

plt.show()