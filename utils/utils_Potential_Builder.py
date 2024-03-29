import numpy as np
import matplotlib.pyplot as plt
class Potential_Builder:
    def __init__(self, obstacle_2d, target_2d):
        self.obstacle = obstacle_2d
        self.target = target_2d
        self.x_range = [-2, 8]
        self.y_range = [-2, 8]
        self.step = 0.1
        self.k_rep = 2
        self.k_att = 2
        self.d0 = 0.5

    def point_to_segment_distance(self, point, segment):
        """计算点到线段的最短距离"""
        p1, p2 = np.array(segment[0]), np.array(segment[1])
        p = np.array(point)
        line_vec = p2 - p1
        p1_to_p = p - p1
        line_len = np.linalg.norm(line_vec)
        line_unitvec = line_vec / line_len
        p1_to_p_scaled = p1_to_p / line_len
        t = np.dot(line_unitvec, p1_to_p_scaled)
        if t < 0.0:
            return np.linalg.norm(p1_to_p)
        elif t > 1.0:
            return np.linalg.norm(p - p2)
        nearest = p1 + line_vec * t
        return np.linalg.norm(p - nearest)

    def point_to_rectangle_distance(self, point, rectangle):
        """计算点到矩形的最短距离"""
        min_distance = float('inf')
        for i in range(len(rectangle)):
            segment = [rectangle[i], rectangle[(i + 1) % len(rectangle)]]
            distance = self.point_to_segment_distance(point, segment)
            min_distance = min(min_distance, distance)
        return min_distance

    def distances_to_rectangles(self, point, rectangles):
        """计算点到一组矩形的距离集合"""
        distances = [self.point_to_rectangle_distance(point, rectangle) for rectangle in rectangles]
        return distances

    def compute_repulsion_force(self, distances, k_rep, d0):
        """计算总斥力，仅考虑大小，不考虑方向"""
        total_repulsion = 0
        for d in distances:
            if d < d0:
                repulsion = 1.0 * k_rep * (1 / d - 1 / d0) ** 2
                total_repulsion += repulsion
        return total_repulsion

    def compute_attraction_potential(self, current_position, goal_position, k_att=0.5):
        """计算吸引势能"""
        # 计算当前位置与目标位置之间的距离
        distance = np.linalg.norm(np.array(current_position) - np.array(goal_position))
        # 计算吸引势能
        attraction_potential = -5 * k_att * (1 / distance)
        return attraction_potential

    def Potential_Build(self):
        x_values = np.arange(self.x_range[0], self.x_range[1], self.step)
        y_values = np.arange(self.y_range[0], self.y_range[1], self.step)
        points = np.transpose([np.tile(x_values, len(y_values)), np.repeat(y_values, len(x_values))])
        points_list = points.tolist()
        potential_energies = []
        for point in points_list:
            distances = self.distances_to_rectangles(point, self.obstacle)
            total_repulsion = self.compute_repulsion_force(distances, self.k_rep, self.d0)
            total_attraction = self.compute_attraction_potential(point, self.target, self.k_att)
            print(total_attraction)
            total_potential = total_repulsion + total_attraction
            potential_energies.append(total_potential)
        x_coords = [point[0] for point in points_list]
        y_coords = [point[1] for point in points_list]
        plt.figure(figsize=(10, 10))
        sc = plt.scatter(x_coords, y_coords, c=potential_energies, cmap='viridis', marker='s', vmin=-20, vmax=10)
        plt.colorbar(sc, label='Potential Energy')
        plt.title('Potential Energy at Different Coordinates')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.show()