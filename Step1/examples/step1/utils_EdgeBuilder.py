import math
class EdgeBuilder:
#  这里的五元组分别为，起始节点，终止节点，地面上物体之间的距离，非地面桑物体直接的距离，堆叠关系,如果边的某一属性不存在则定义为-1
    def __init__(self, object_stacking):
        self.object_stacking = object_stacking
        self.edges = []  # List to store all edges

    def is_fully_covered(self, A, B):
        # 分别获取A和B在x, y轴的最小值和最大值
        Ax_min, Ay_min, _, Ax_max, Ay_max, _ = A
        Bx_min, By_min, _, Bx_max, By_max, _ = B

        # 检查A是否完全覆盖B或者B是否完全覆盖A在x轴和y轴上
        A_covers_B_x = Ax_min <= Bx_min and Ax_max >= Bx_max
        A_covers_B_y = Ay_min <= By_min and Ay_max >= By_max
        B_covers_A_x = Bx_min <= Ax_min and Bx_max >= Ax_max
        B_covers_A_y = By_min <= Ay_min and By_max >= Ay_max

        return (A_covers_B_x and A_covers_B_y) or (B_covers_A_x and B_covers_A_y)

    def calculate_distance(self, position1, position2):
        # 计算两点之间的欧式距离
        return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(position1, position2)))

    def build_edges(self):
        # 对于object_stacking中的每个对象（起点）
        for i, start_obj in enumerate(self.object_stacking):
            for j, end_obj in enumerate(self.object_stacking):
                if i == j:
                    continue
                start_name, start_position, start_range, start_bool = start_obj
                end_name, end_position, end_range, end_bool = end_obj
                if start_bool and end_bool:
                    distance1 = self.calculate_distance(start_position, end_position)
                    distance2 = None
                    is_stacked = False
                elif not start_bool and not end_bool:
                    distance1 = None
                    distance2 = self.calculate_distance(start_position, end_position)
                    is_stacked = False
                else:
                    distance1 = None
                    distance2 = None
                    is_stacked = self.is_fully_covered(start_range, end_range)
                edge = {
                    'start': start_name,
                    'end': end_name,
                    'distance1': distance1,
                    'distance2': distance2,
                    'is_stacked': is_stacked
                }
                self.edges.append(edge)

    def normalize_and_weight_edges(self, weight_distance1=2, weight_distance2=1, weight_is_stacked=5):
        if not self.edges:
            self.build_edges()
        # 初始化最大最小值
        max_distance1 = max(edge['distance1'] for edge in self.edges if edge['distance1'] is not None)
        min_distance1 = min(edge['distance1'] for edge in self.edges if edge['distance1'] is not None)
        max_distance2 = max(edge['distance2'] for edge in self.edges if edge['distance2'] is not None)
        min_distance2 = min(edge['distance2'] for edge in self.edges if edge['distance2'] is not None)

        # 遍历每条边，归一化并加权
        for edge in self.edges:
            # 归一化distance1
            if edge['distance1'] is not None:
                norm_distance1 = (edge['distance1'] - min_distance1) / (max_distance1 - min_distance1) * weight_distance1
            else:
                norm_distance1 = 0

            # 归一化distance2
            if edge['distance2'] is not None:
                norm_distance2 = (edge['distance2'] - min_distance2) / (max_distance2 - min_distance2) * weight_distance2
            else:
                norm_distance2 = 0

            # 加权is_stacked
            norm_is_stacked = 1 if edge['is_stacked'] else 0
            norm_is_stacked *= weight_is_stacked

            # 计算加权的边权重
            edge_weight = norm_distance1 + norm_distance2 + norm_is_stacked
            edge['weight'] = edge_weight

    def get_edges(self):
        # 返回所有创建的边
        return self.edges


