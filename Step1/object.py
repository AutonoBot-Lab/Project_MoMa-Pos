class Table:
    def __init__(self, coordinates, distance_to_length, distance_to_width):
        self.coordinates = coordinates  # 坐标
        self.distance_to_length = distance_to_length  # 中心点到长的距离
        self.distance_to_width = distance_to_width  # 中心点到宽的距离

    def __repr__(self):
        return f"Table(coordinates={self.coordinates}, distance_to_length={self.distance_to_length}, distance_to_width={self.distance_to_width})"

class Bowl:
    def __init__(self, coordinates,distance_to_length=0.02,distance_to_width=0.02):
        self.coordinates = coordinates  # 坐标
        self.distance_to_length = distance_to_length  # 中心点到长的距离
        self.distance_to_width = distance_to_width
    def __repr__(self):
        return f"Bowl(coordinates={self.coordinates})"

class Checker:
    @staticmethod
    def is_bowl_on_table(table, bowl):
        x, y = bowl.coordinates
        table_x, table_y = table.coordinates
        
        # 计算table的边界坐标
        x_min = table_x - table.distance_to_length
        x_max = table_x + table.distance_to_length
        y_min = table_y - table.distance_to_width
        y_max = table_y + table.distance_to_width
        
        # 检查bowl的坐标是否在table的范围内
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return 1
        else:
            return 0
        
    def whether_on_each_other(table_base, table_compared):
        base_x_min = table_base.coordinates[0] - table_base.distance_to_length
        base_x_max = table_base.coordinates[0] + table_base.distance_to_length
        base_y_min = table_base.coordinates[1] - table_base.distance_to_width
        base_y_max = table_base.coordinates[1] + table_base.distance_to_width
        
        # 计算对比table的四个角点
        compared_corners = [
            (table_compared.coordinates[0] - table_compared.distance_to_length, table_compared.coordinates[1] - table_compared.distance_to_width),
            (table_compared.coordinates[0] - table_compared.distance_to_length, table_compared.coordinates[1] + table_compared.distance_to_width),
            (table_compared.coordinates[0] + table_compared.distance_to_length, table_compared.coordinates[1] - table_compared.distance_to_width),
            (table_compared.coordinates[0] + table_compared.distance_to_length, table_compared.coordinates[1] + table_compared.distance_to_width),
        ]
        
        # 检查所有角点是否在基础table的范围内
        return all(base_x_min <= x <= base_x_max and base_y_min <= y <= base_y_max for x, y in compared_corners)
    
    def __repr__(self):
        return f"Table(({self.coordinates[0]},{self.coordinates[1]}),{self.distance_to_length},{self.distance_to_width})"
   








