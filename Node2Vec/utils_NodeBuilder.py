import math
class NodeBuilder:
    def __init__(self, object_node):
        self.object_node = object_node
        self.nodes = []

    def build_nodes(self):
        # 遍历每一个节点
        for node in self.object_node:
            # 解析节点信息
            name, position, size, is_stacked = node

            # 创建节点属性字典
            node_attributes = {
                'position': position,  # 节点位置
                'size': size,          # 节点尺寸
                'is_stacked': is_stacked  # 节点是否堆叠
            }

            # 将节点及其属性添加到节点列表中
            self.nodes.append((name, node_attributes))

    def get_nodes(self):
        # 调用构建节点的函数
        self.build_nodes()
        # 返回构建好的节点列表
        return self.nodes
