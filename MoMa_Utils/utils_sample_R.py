import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon
import time
from rtree import index
import heapq
import random

class Sample:
    
    def __init__(self, target_2d, obstacle_2d, l1, l2, base_length):
        self.target_2d = target_2d  # 目标x-y平面坐标
        self.l1 = l1    # 最小长度  
        self.l2 = l2    # 最大长度
        self.radius = base_length / 2   # base半径
        self.final_candidates = []  # 候选点
        
        # 创建 R-tree 索引,插入所有障碍物矩形框
        self.obstacle_index = index.Index()
        for i, obstacle in enumerate(obstacle_2d):
            self.obstacle_index.insert(i, coordinates=Polygon(obstacle).bounds)

    # 判断机器人当前位置的base边界与障碍物边界是否存在重合
    def is_inside_base(self, x, y):
        # 生成当前机器人base边界框
        rect = Polygon([
            (x - self.radius, y - self.radius),
            (x + self.radius, y - self.radius),
            (x + self.radius, y + self.radius),
            (x - self.radius, y + self.radius)
        ])

        # 查询与base边界框相交的障碍物矩形框索引
        id_list = list(self.obstacle_index.intersection(rect.bounds))
        if len(id_list) > 0:    # 有相交的障碍物矩形框
            return False
        return True

    # 生成指定数量的可行点Habitat
    def generate_habitat_X_points(self):
        Table_x = np.linspace(0, 4, 40)
        Table_y = np.linspace(0, 4, 40)
        Drawer_x = np.linspace(2, 4.5, 40)
        Drawer_y = np.linspace(1.5, 3.5, 40)
        Fridge_x = np.linspace(2, 4.5, 40)
        Fridge_y = np.linspace(4, 6, 40)
        B1_x = np.linspace(3, 5, 40)
        B1_y = np.linspace(3, 5, 40)
        B2_x = np.linspace(3, 5, 40)
        B2_y = np.linspace(4, 6, 40)
        Dishwash_x = np.linspace(2, 4, 40)
        Dishwash_y = np.linspace(2, 4, 40)

        for i in Table_x:
            for j in Table_y:
                if self.is_inside_base(i, j):
                    self.final_candidates.append([i, j])
        return self.final_candidates

    def generate_reuleaux_points(self, con_map):
        remain_map = {}
        for key, value in con_map.items():
            x, y = key
            if self.is_inside_base(x, y):
                remain_map[key] =value
                # 检查值不为6的元素个数是否等于remain_map中的元素总数
        n = 5
        if all(value == 6 for value in remain_map.values()):

            # 计算每个点到target_2d的距离
            distances = {key: np.linalg.norm(np.array(key) - np.array(self.target_2d)) for key in remain_map.keys()}
            # 找到距离最近的点的二维坐标
            closest_points = heapq.nsmallest(n, distances, key=lambda x: distances[x])
            closest_points = [list(point) for point in closest_points]
            return closest_points
        # else:
        #     min_value = min(remain_map.values())
        #     min_value_keys = [key for key, value in remain_map.items() if value == min_value]
        #     if len(min_value_keys) > 5:
        #         closest_points = random.sample(min_value_keys, 5)
        #     else:
        #         closest_points = min_value_keys
        #     closest_points = [list(point) for point in closest_points]
        #     return closest_points
        else:
            closest_points = []
            sorted_values = sorted(set(remain_map.values()))
            for value in sorted_values:
                keys_with_value = [key for key, val in remain_map.items() if val == value]
                if len(keys_with_value) + len(closest_points) > n:
                    closest_points.extend(random.sample(keys_with_value, n - len(closest_points)))
                    break
                else:
                    closest_points.extend(keys_with_value)
            closest_points = [list(point) for point in closest_points[:n]]
            return closest_points
    def euclidean_distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def generate_habitat_Y_points(self):
        Table_x = np.linspace(0, 4, 40)
        Table_y = np.linspace(0, 4, 40)
        Drawer_x = np.linspace(2, 4.5, 40)
        Drawer_y = np.linspace(1.5, 3.5, 40)
        Fridge_x = np.linspace(2, 4.5, 40)
        Fridge_y = np.linspace(4, 6, 40)
        B1_x = np.linspace(3, 5, 40)
        B1_y = np.linspace(3, 5, 40)
        B2_x = np.linspace(3, 5, 40)
        B2_y = np.linspace(4, 6, 40)
        Dishwash_x = np.linspace(2, 4, 40)
        Dishwash_y = np.linspace(2, 4, 40)

        for i in B2_x:
            for j in B2_y:
                if self.is_inside_base(i, j):
                    self.final_candidates.append([i, j])
        self.final_candidates = heapq.nsmallest(5, self.final_candidates, key=lambda point: self.euclidean_distance(point, self.target_2d))
        return self.final_candidates

    def generate_habitat_Y_counter_points(self):
        # Habitat_Y counter
        H_Drawer_X = np.linspace(2.8, 2.8, 1)
        H_Drawer_Y = np.linspace(2, 2.8, 20)
        H_Fridge_X = np.linspace(3.1, 3.1, 1)
        H_Fridge_Y = np.linspace(5.5, 6, 20)
        H_Dishwash_X = np.linspace(2.76, 2.76, 1)
        H_Dishwash_Y = np.linspace(3, 3.8, 20)
        # 生成所有可能的坐标组合
        X, Y = np.meshgrid(H_Fridge_X, H_Fridge_Y)
        all_coords = np.array([X.ravel(), Y.ravel()]).T  # 转换为(N, 2)数组，N是所有可能坐标的数量

        # 随机选取五个坐标
        np.random.seed(int(time.time()))  # 设置随机种子以便复现结果
        selected_indices = np.random.choice(all_coords.shape[0], 20, replace=False)
        self.final_candidates = all_coords[selected_indices]
        self.final_candidates = self.final_candidates.tolist()
        return self.final_candidates

    # 生成指定数量的可行点MoMa_Pos
    def generate_enough_points(self):
        target_count = 50
        s1 = time.time()
        cnt = 0
        while len(self.final_candidates) < target_count:
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(self.l1, self.l2)
            x = self.target_2d[0] + radius * np.cos(angle)
            y = self.target_2d[1] + radius * np.sin(angle)
            if self.is_inside_base(x, y):   # 如果与障碍物没有重合,接收
                self.final_candidates.append([x, y])
            cnt += 1
        s2 = time.time()
        # print('生成可行点尝试次数:', cnt)
        print('生成可行点时间为:', s2-s1)
        return self.final_candidates