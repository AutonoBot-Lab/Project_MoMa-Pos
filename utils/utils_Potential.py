import numpy as np
import math
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
class Potential:
    def __init__(self, remaining_points, obstacle_3d, obstacle_2d, target_3d):
        self.remaining_points = remaining_points
        self.obstacle_3d = obstacle_3d
        self.obstacle_2d = obstacle_2d
        self.target_3d = target_3d
        self.extended_point = []
        self.updated_sets = []
        self.potential = []
        self.face = []
    # [0.4, 1, 1.4]
    def expand_with_z(self, z_values=[0.8]):
        for point in self.remaining_points:
            self.extended_point.append([[point[0], point[1], z] for z in z_values])
        for cube_vertices in self.obstacle_3d:
            faces = self.is_segment_through_cube(cube_vertices)
            for face in faces:
                self.face.append(face)

    def Potential_Build(self, point_i):
        bool_i = True
        for face in self.face:
            if not self.line_plane_intersection([point_i, self.target_3d], face):
                bool_i = False
                break
        return bool_i

    def process_coordinates(self):
        # start_time = time.time()
        for coord_set in self.extended_point:
            updated_set = []
            for coord in coord_set:
                potential_bool = self.Potential_Build(coord)
                updated_set.append(coord + [potential_bool])
            self.updated_sets.append(updated_set)
        # end_time = time.time()
        for lst_i in self.updated_sets:
            list = self.calculate_potential_from_list(lst_i, self.target_3d)
            self.potential.append(list)
        # self.draw_potential_map()

        # elapsed_time = end_time - start_time
        # print(f"代码执行时间：{elapsed_time}秒")
        return self.potential
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
                distance = math.sqrt(
                    (item[0] - target[0]) ** 2 + (item[1] - target[1]) ** 2 + (item[2] - target[2]) ** 2)
                potential_value = 1 / distance if distance != 0 else float('inf')  # 计算距离的倒数作为势能值
            else:
                potential_value = 0

            potential_dict[key] = potential_dict.get(key, 0) - potential_value  # 累加势能值

        return potential_dict

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

    def line_plane_intersection(self, line, plane, tolerance=1e-3):
        line_z_min, line_z_max = min(line[0][2], line[1][2]), max(line[0][2], line[1][2])
        line_y_min, line_y_max = min(line[0][1], line[1][1]), max(line[0][1], line[1][1])
        line_x_min, line_x_max = min(line[0][0], line[1][0]), max(line[0][0], line[1][0])

        plane_z_values = [point[2] for point in plane]
        plane_y_values = [point[1] for point in plane]
        plane_x_values = [point[0] for point in plane]

        plane_z_min, plane_z_max = min(plane_z_values), max(plane_z_values)
        plane_y_min, plane_y_max = min(plane_y_values), max(plane_y_values)
        plane_x_min, plane_x_max = min(plane_x_values), max(plane_x_values)


        if line_z_max < plane_z_min or line_z_min > plane_z_max:
            return True
        if line_y_max < plane_y_min or line_y_min > plane_y_max:
            return True
        if line_x_max < plane_x_min or line_x_min > plane_x_max:
            return True
        # 计算平面法向量
        plane_normal = np.cross(np.subtract(plane[1], plane[0]), np.subtract(plane[2], plane[0]))
        plane_point = np.array(plane[0])

        # 直线的方向向量
        line_dir = np.subtract(line[1], line[0])
        line_point = np.array(line[0])

        # 检查直线和平面是否平行
        dot_product = np.dot(line_dir, plane_normal)
        if abs(dot_product) < tolerance:  # 考虑误差
            return True  # 直线和平面平行或重合
        # 计算交点
        t = np.dot(plane_normal, np.subtract(plane_point, line_point)) / dot_product
        intersection_point = line_point + t * line_dir
        inter_point_bool = self.is_point_in_line_segment(intersection_point, line) and self.is_point_in_rectangle(intersection_point, plane)

        if inter_point_bool:
            return False
        else:
            return True
    def is_point_in_line_segment(self, intersection_point, line, tolerance=1e-3):
        """检查点是否在直线段内"""
        """如果这个点确实在这个线段内（包括端点），函数返回 True；否则返回 False"""
        p1, p2 = np.array(line[0]), np.array(line[1])
        ip = np.array(intersection_point)
        dist_p1_ip = np.linalg.norm(ip - p1)
        dist_p2_ip = np.linalg.norm(ip - p2)
        dist_p1_p2 = np.linalg.norm(p2 - p1)

        return abs((dist_p1_ip + dist_p2_ip) - dist_p1_p2) < tolerance

    def is_point_in_rectangle(self, intersection_point, rectangle, tolerance=1e-6):
        """检查点是否在矩形内部"""
        """"如果点在矩形内部（包括边界），函数返回 True；否则返回 False"""
        ip = np.array(intersection_point)

        for i in range(4):
            p1, p2 = np.array(rectangle[i]), np.array(rectangle[(i + 1) % 4])
            edge = p2 - p1
            to_point = ip - p1

            if np.dot(np.cross(edge, to_point), np.cross(edge, np.array(rectangle[(i + 2) % 4]) - p1)) < -tolerance:
                return False

        return True

