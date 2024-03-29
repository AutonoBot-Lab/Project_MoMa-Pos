import math
class EdgeBuilder:
#  这里的五元组分别为，起始节点，终止节点，地面上物体之间的距离，非地面桑物体直接的距离，堆叠关系,如果边的某一属性不存在则定义为-1
    def __init__(self, object_stacking):
        self.object_stacking = object_stacking
        self.edges = []  # List to store all edges
        self.end_value = None
    def is_within(self, A, B):
        Ax_min, Ay_min, _, Ax_max, Ay_max, _ = A
        Bx_min, By_min, _, Bx_max, By_max, _ = B
        B_covers_A_x = Bx_min <= Ax_min and Bx_max >= Ax_max
        B_covers_A_y = By_min <= Ay_min and By_max >= Ay_max
        return B_covers_A_x and B_covers_A_y

    def edge_attribute_add(self):
        updated_object_stacking = []
        for obj_start in self.object_stacking:
            start_name, start_position, start_dimensions, start_is_on_ground = obj_start
            if start_is_on_ground:
                updated_object_stacking.append(obj_start + ('ground',))
            else:
                for obj_end in self.object_stacking:
                    end_name, end_position, end_dimensions, end_is_on_ground = obj_end
                    if start_name == end_name:
                        continue
                    else:
                        if self.is_within(start_dimensions, end_dimensions):
                            updated_object_stacking.append(obj_start + (end_name,))
                            break
                        else:
                            continue
        self.object_stacking = updated_object_stacking
        return updated_object_stacking

    def get_end_value(self):
        for i, items in enumerate(self.object_stacking):
            items_name, items_position, items_range, items_bool, items_on = items
            if items_name == 'Bowl_Target':
                self.end_value = items_on
                break

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
        dis = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(position1, position2)))
        dis_change = 1/dis
        return dis_change

    def build_new_edges(self):

        for i, start_obj in enumerate(self.object_stacking):
            for j, end_obj in enumerate(self.object_stacking):
                if i == j:
                    continue
                start_name, start_position, start_range, start_bool, start_on = start_obj
                end_name, end_position, end_range, end_bool, end_on = end_obj
                # and (start_name == self.end_value or end_name == self.end_value)
                if start_bool and end_bool and (start_name == self.end_value or end_name == self.end_value):
                    distance1 = self.calculate_distance(start_position, end_position)
                    distance2 = None
                    is_stacked = 0
                    X_min, Y_min, _, X_max, Y_max, _ = end_range
                    X_range = X_max - X_min
                    Y_range = Y_max - Y_min
                    end_size = X_range * Y_range
                    self.edges.append({
                        'start': start_name,
                        'end': end_name,
                        'distance1': distance1,
                        'distance2': distance2,
                        'is_stacked': is_stacked,
                        'size': end_size
                    })
                # elif start_name == "Bowl_Target" and start_on == end_name:
                elif not start_bool and start_on == end_name:
                    # if start_name == "Bowl_Target":
                    distance1 = None
                    distance2 = None
                    is_stacked = 1
                    end_size = 0
                    self.edges.append({
                        'start': start_name,
                        'end': end_name,
                        'distance1': distance1,
                        'distance2': distance2,
                        'is_stacked': is_stacked,
                        'size': end_size
                    })
                    # else:
                    #     distance1 = None
                    #     distance2 = None
                    #     is_stacked = 1
                    #     self.edges.append({
                    #         'start': start_name,
                    #         'end': end_name,
                    #         'distance1': distance1,
                    #         'distance2': distance2,
                    #         'is_stacked': is_stacked
                    #     })

                elif not start_bool and not end_bool and start_on == end_on and end_on == self.end_value and end_name =='Bowl_Target' :
                    distance1 = None
                    distance2 = self.calculate_distance(start_position, end_position)
                    is_stacked = 0
                    end_size = 0
                    self.edges.append({
                        'start': start_name,
                        'end': self.end_value,
                        'distance1': distance1,
                        'distance2': distance2,
                        'is_stacked': is_stacked,
                        'size': end_size
                    })

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

    def normalize_and_weight_edges(self, weight_distance1=10, weight_distance2=0, weight_is_stacked=1, weight_size=0):
        if not self.edges:
            self.build_edges()
        # 初始化最大最小值
        max_distance1 = max(edge['distance1'] for edge in self.edges if edge['distance1'] is not None)
        min_distance1 = min(edge['distance1'] for edge in self.edges if edge['distance1'] is not None)
        if any(edge['distance2'] is not None for edge in self.edges):
            max_distance2 = max(edge['distance2'] for edge in self.edges if edge['distance2'] is not None)
            min_distance2 = min(edge['distance2'] for edge in self.edges if edge['distance2'] is not None)
        else:
            norm_distance2 = 0.0001
        max_size = max(edge['size'] for edge in self.edges if edge['size'] is not None)
        min_size = min(edge['size'] for edge in self.edges if edge['size'] is not None)
        # 遍历每条边，归一化并加权
        for edge in self.edges:
            # 归一化distance1
            if edge['distance1'] is not None:
                norm_distance1 = (edge['distance1'] - min_distance1) / (max_distance1 - min_distance1) * weight_distance1
            else:
                norm_distance1 = 0.00001

            # 归一化distance2
            if edge['distance2'] is not None:
                norm_distance2 = (edge['distance2'] - min_distance2) / (max_distance2 - min_distance2) * weight_distance2
            else:
                norm_distance2 = 0.00001

            # 加权is_stacked
            norm_is_stacked = edge['is_stacked']
            norm_is_stacked *= weight_is_stacked

            if edge['size'] is not None:
                norm_size = (edge['size'] - min_size) / (max_size - min_size) * weight_size
            else:
                norm_size = 0.0001

            # 计算加权的边权重
            edge_weight = norm_distance1 + norm_distance2 + norm_is_stacked + norm_size
            edge['weight'] = edge_weight

    def get_edges(self):
        # 返回所有创建的边
        return self.edges


