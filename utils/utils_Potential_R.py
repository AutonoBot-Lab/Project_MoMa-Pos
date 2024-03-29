import numpy as np
import math
import time
from itertools import chain
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Potential:
    
    def __init__(self, remaining_points, obstacle_3d, obstacle_2d, target_3d):
        self.remaining_points = remaining_points  # 生成的候选点
        self.obstacle_3d = obstacle_3d  # 障碍物的三维长方体对象
        self.obstacle_2d = obstacle_2d  # 障碍物的二维矩形对象
        self.target_3d = target_3d  # 目标位置
        self.extended_point = []    # z轴扩展后的候选点
        self.updated_sets = []  # 带是否碰撞标志的候选点坐标
        self.potential = []     # x-y平面上的候选点势能
        self.face = []  # 所有障碍物的面

    # 将所有采样点在z轴上进行扩展[0.4, 1, 1.4]
    def expand_with_z(self, z_values=[0.4, 1, 1.4]):
        self.extended_point = [[[point[0], point[1], z] for z in z_values] for point in self.remaining_points]
        faces = [self.is_segment_through_cube(cube_vertices) for cube_vertices in self.obstacle_3d]
        self.face = list(chain.from_iterable(faces))

    # 判断当前与目标位置构成线段是否与某障碍物面相交
    def Potential_Build(self, point):
        for face in self.face:  # 与某一个面相交就返回False
            if self.line_plane_intersection([point, self.target_3d], face):
                return False
        return True
    
    # 计算x-y平面上所有点的累加势能并可视化
    def process_coordinates(self, display):  
        start_time = time.time()
        self.updated_sets = [[coord + [self.Potential_Build(coord)] for coord in coord_set] for coord_set in self.extended_point]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"计算所有势能耗时:{elapsed_time}秒")
        self.potential = [self.calculate_potential_from_list(lst_i, self.target_3d) for lst_i in self.updated_sets]
        if display: self.draw_potential_map()
        return self.potential
    
    # 可视化势能图
    def draw_potential_map(self):
        x_coords, y_coords, potentials = [], [], []
        for d in self.potential:
            for key, value in d.items():
                x_coords.append(key[0])
                y_coords.append(key[1])
                potentials.append(value)
        target_coord = self.target_3d[:2]
        plt.figure(figsize=(10, 8))
        for rect in self.obstacle_2d:
            rectangle = Rectangle((rect[0][0], rect[0][1]), rect[2][0] - rect[0][0], rect[2][1] - rect[0][1],
                                  edgecolor='gray', facecolor='none')
            plt.gca().add_patch(rectangle)
        sc = plt.scatter(x_coords, y_coords, c=potentials, cmap='viridis', marker='s', vmin=-3, vmax=0, s=10)
        plt.colorbar(sc, label='Potential Energy')
        plt.scatter(*target_coord, color='red', marker='o')
        plt.title('Potential Energy Map')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim([-1.02, 7.2])
        plt.ylim([0, 7])
        plt.grid(False)
        # plt.savefig('/home/sc-5/Desktop/shao/BestMan_Pybullet/MoMa_Pos/Step2_Picture/drawer4.png', dpi=1000)
        plt.show()
        
    def calculate_potential_from_list(self, lst, target):
        """
        计算列表中每个元素对应的势能值。

        :param lst: 输入列表，例如 [[3.5, 5.5, 0.5, False], [3.5, 5.5, 1, True], ...]。
        :param target: 目标三维坐标点，例如 [1, 1, 1]。
        :return: 以前两个维度为键，累加势能值为值的字典。
        """

        potential_dict = {}

        for item in lst:
            
            key = tuple(item[:2])  # 提取前两个维度作为键
            if item[3]:  # 如果第四个维度是 True
                distance = math.sqrt((item[0] - target[0]) ** 2 + (item[1] - target[1]) ** 2 + (item[2] - target[2]) ** 2)
                potential_value = 1 / distance if distance != 0 else float('inf')  # 计算距离的倒数作为势能值
            else:
                potential_value = 0

            potential_dict[key] = potential_dict.get(key, 0) - potential_value  # 累加势能值

        return potential_dict
    
    # 根据长方体的八个点创建六个面
    def is_segment_through_cube(self, cube_vertices):
        faces = [
            [cube_vertices[0], cube_vertices[1], cube_vertices[2], cube_vertices[3]],  # 底面
            [cube_vertices[4], cube_vertices[5], cube_vertices[6], cube_vertices[7]],  # 顶面
            [cube_vertices[0], cube_vertices[1], cube_vertices[5], cube_vertices[4]],  # 侧面1
            [cube_vertices[1], cube_vertices[2], cube_vertices[6], cube_vertices[5]],  # 侧面2
            [cube_vertices[2], cube_vertices[3], cube_vertices[7], cube_vertices[6]],  # 侧面3
            [cube_vertices[3], cube_vertices[0], cube_vertices[4], cube_vertices[7]],  # 侧面4
        ]
        return faces
    
    # 判断线段与四个顶点定义的方形区域是否相交,近似平行不算相交
    def line_plane_intersection(self, line, plane, tolerance=1e-3):
        
        '''关键加快判断的代码块,线段的包围盒是否与平面的包围盒相交'''
        # TODO: 这部分可以继续优化,但是numpy重写效果反而变差
        line_z_min, line_z_max = min(line[0][2], line[1][2]), max(line[0][2], line[1][2])
        line_y_min, line_y_max = min(line[0][1], line[1][1]), max(line[0][1], line[1][1])
        line_x_min, line_x_max = min(line[0][0], line[1][0]), max(line[0][0], line[1][0])

        plane_z_values = [point[2] for point in plane]
        plane_y_values = [point[1] for point in plane]
        plane_x_values = [point[0] for point in plane]

        plane_z_min, plane_z_max = min(plane_z_values), max(plane_z_values)
        plane_y_min, plane_y_max = min(plane_y_values), max(plane_y_values)
        plane_x_min, plane_x_max = min(plane_x_values), max(plane_x_values)

        # 获取plane的最小与最大边界
        # plane_min = np.min(plane, axis=0)
        # plane_max = np.max(plane, axis=0)
        if line_z_max < plane_z_min or line_z_min > plane_z_max or line_y_max < plane_y_min or line_y_min > plane_y_max or line_x_max < plane_x_min or line_x_min > plane_x_max:
            return False
        
        '''线段与矩形是否相交'''
        p0, p1 = np.array(line)     # 线段的两个端点
        direction = p1 - p0                # 线段的方向向量
        
        v0, v1, v2, v3 = plane  # 方形区域的四个顶点
        e1, e2 = v1 - v0, v2 - v1                # 矩形边向量AB, BC
        normal = np.cross(e1, e2)                # 平面的法向量
        
        # 判断线段与平面法向量是否平行,考虑误差
        dot_product = np.dot(direction, normal)
        if abs(dot_product) < tolerance:    # 平行则不相交,返回False
            return False    
        
        # 计算线段与平面的交点参数
        t = np.dot((v0 - p0), normal) / dot_product
        
        if 0 <= t <= 1:     # 不平行就一定有交点,只是可能在线段延长线上,检查交点是否位于线段上,只有参数t在0~1的范围内说明线段与平面有交点且在线段内,但是交点还可能在矩形外
            
            intersection_point = p0 + t * direction      # 计算交点坐标
            '''
                判断交点是否在矩形ABCD内,需要 (AB X AP) * (CD X CP) >= 0、(BC X BP) * (DA X DP) >= 0
                根据向量的叉乘性, (AB X AP) * (CD X CP) >= 0 保证 P 在 AB 和 CD 之间, (BC X BP) * (DA X DP) >= 0 保证 P 在 BC 和 DA 之间, 这样可以保证 P 落在矩形范围内
            '''
            e3, e4 = v3 - v2, v0 - v3    # 矩形边向量CD,DA
            f1, f2, f3, f4 = intersection_point - v0, intersection_point - v1, intersection_point - v2, intersection_point - v3   # 矩形四顶点指向交点的向量
            if np.dot(np.cross(e1, f1), np.cross(e3, f3)) >= 0 and np.dot((np.cross(e2, f2)), np.cross(e4, f4)) >= 0:
                return True
            return False    # 不满足就说明交点落在矩形外,线段与矩形不相交
        
        return False

