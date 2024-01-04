import networkx as nx
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
            start, end= edge['start'], edge['end']
            # 设置边的属性，比如距离和是否堆叠
            attributes = {k: v for k, v in edge.items() if k in ['weight']}
            self.G.add_edge(start, end, **attributes)

        return self.G