import numpy as np

# 设置范围和步长
x_range = (1, 6)
y_range = (4, 8)
step = 0.05

# 构建集合
x_values = np.arange(x_range[0], x_range[1], step)
y_values = np.arange(y_range[0], y_range[1], step)
points = np.transpose([np.tile(x_values, len(y_values)), np.repeat(y_values, len(x_values))])

points_list = points.tolist()
print(len(points_list))