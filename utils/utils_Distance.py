import math
import numpy as np
import matplotlib.pyplot as plt
import heapq
class Distance:
    def __init__(self, potential_map, init_pos):
        self.remain_potential_map = potential_map
        self.potential_map = potential_map
        self.init_pos = init_pos
        self.init_pos = {tuple(self.init_pos): 0}
        self.num_point = 5
        self.multiple = 24
        # dist_k = 5/6
        self.dist_k = 5/6
        self.potential_k = 1-self.dist_k
        self.matrix = None
    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def cal_distance(self):
        # self.potential_map = [item for item in self.potential_map if list(item.values())[0] < self.threshold]
        # self.remain_potential_map = [item for item in self.remain_potential_map if list(item.values())[0] >= self.threshold]
        # 查找与 init_pos 距离最近的元素
        self.potential_map = [item for item in self.potential_map if list(item.values())[0] < 0]
        self.potential_map = heapq.nsmallest(self.num_point, self.potential_map, key=lambda x: list(x.values())[0])
        self.potential_map.insert(0, self.init_pos)

        points_values = [(list(item.keys())[0], list(item.values())[0]) for item in self.potential_map]
        n = len(points_values)
        distance_matrix = np.full((n, n), np.inf)
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist = self.euclidean_distance(points_values[i][0], points_values[j][0]) + 3
                    adjusted_dist = self.dist_k * dist - self.potential_k * (points_values[i][1] - points_values[j][1])
                    distance_matrix[i][j] = adjusted_dist * self.multiple
        distance_matrix = np.round(distance_matrix, 2)
        self.matrix = distance_matrix
        self.convert_to_valid_python_list()
        # return distance_matrix
    def convert_to_valid_python_list(self):
        matrix = []
        # 遍历 numpy 数组的每一行
        for row in self.matrix:
            # 将每一行转换为 Python 列表
            python_row = [x if x != np.inf else float('inf') for x in row]
            matrix.append(python_row)

        self.matrix = matrix
        return self.matrix
    def draw_order_picture(self, order):
        coords = [list(point.keys())[0] for point in self.potential_map]
        potentials = [list(point.values())[0] for point in self.potential_map]
        coords_remain = [list(point.keys())[0] for point in self.remain_potential_map]
        potentials_remain = [list(point.values())[0] for point in self.remain_potential_map]
        x, y = zip(*coords)
        ordered_x = [x[i - 1] for i in order]  # 减1因为列表索引是从0开始的
        ordered_y = [y[i - 1] for i in order]

        x_remain, y_remain = zip(*coords_remain)


        # 设置颜色映射
        sc = plt.scatter(x, y, c=potentials, cmap='viridis', marker='s', vmin=-3, vmax=0, s=20)
        sc_re = plt.scatter(x_remain, y_remain, c=potentials_remain, cmap='viridis', marker='s', vmin=-3, vmax=0, s=20)
        # 绘制连接线
        # plt.scatter(self.init_pos[0], self.init_pos[1], color='red', marker='o', s=50)  # 红色点，较大的尺寸
        plt.plot(ordered_x, ordered_y, color='red', linestyle='-', linewidth=1)
        # 添加颜色条
        plt.colorbar(sc, label='Potential')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim([-1.02, 7.2])
        plt.ylim([0, 7])
        plt.title('Points and Connections with Square Markers')
        # 显示图表
        plt.show()

