import networkx as nx
import random
class GraphBuilder:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.G = nx.DiGraph()

    def build_Graph(self):
        for node, attributes in self.nodes:
            self.G.add_node(node, **attributes)

        # 添加边
        for edge in self.edges:
            start, end = edge['start'], edge['end']
            # 设置边的属性，比如距离和是否堆叠
            attributes = {k: v for k, v in edge.items() if k in ['weight']}
            self.G.add_edge(start, end, **attributes)

        for edge in self.edges:
            start, end, weight = edge['start'], edge['end'], edge['weight']
            # 确认图中有这条边，并且边包含权重属性
            if self.G.has_edge(start, end):
                self.G[start][end]['weight'] = weight
        return self.G

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge['start'] == node:
                neighbors.append(edge['end'])
        return neighbors

    def random_walk(self, node, walk_length):
        walk = [node]
        for _ in range(walk_length - 1):
            current = walk[-1]
            neighbors = self.get_neighbors(current)
            weights = [self.G[current][neighbor]['weight'] for neighbor in neighbors]

            # 生成随机游走概率分布
            total_weight = sum(weights)
            probabilities = [weight/total_weight for weight in weights]

            # 根据边权重随机选择下一个节点
            if neighbors:
                next_node = random.choices(neighbors, weights=probabilities)[0]
                walk.append(next_node)
            else:
                break

        return walk