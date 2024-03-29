import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon
class Sample:
    def __init__(self, target_2d, obstacle_2d, l1, l2, base_length):
        self.target_2d = target_2d
        self.obstacle_2d = obstacle_2d
        self.obstacle_polygons = [Polygon(obstacle) for obstacle in obstacle_2d]
        self.l1 = l1
        self.l2 = l2
        self.length = base_length
        self.final_candidates = []


    def is_inside_base(self, point):
        x, y = point
        rect = Polygon([
            (x - self.length / 2, y - self.length / 2),
            (x + self.length / 2, y - self.length / 2),
            (x + self.length / 2, y + self.length / 2),
            (x - self.length / 2, y + self.length / 2)
        ])
        for obstacle_rect in self.obstacle_polygons:
            if rect.intersects(obstacle_rect):
                return False
        return True


    def generate_enough_points(self):
        target_count = 50
        while len(self.final_candidates) < target_count:
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(self.l1, self.l2)
            x = self.target_2d[0] + radius * np.cos(angle)
            y = self.target_2d[1] + radius * np.sin(angle)
            point = [x, y]
            if self.is_inside_base(point):
                self.final_candidates.append(point)
        return self.final_candidates