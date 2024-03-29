import math
import sys
import os
import pybullet as p
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from node2vec import Node2Vec
from gensim.models import Word2Vec
"""
Get the utils module path
"""
# customized package
current_path = os.path.abspath(__file__)
utils_path = os.path.dirname(os.path.dirname(current_path)) + '/utils'
if os.path.basename(utils_path) != 'utils':
    raise ValueError('Not add the path of folder "utils", please check again!')
sys.path.append(utils_path)
from utils_PbClient import PbClient
from utils_PbVisualizer import PbVisualizer
from utils_EdgeBuilder import EdgeBuilder
from utils_NodeBuilder import NodeBuilder
from utils_Graph import GraphBuilder
from utils_SortSimilarity import Sort_Similarity
# load kitchen from three scenarios
index = 2
if index == 0:
    from utils_Kitchen_v0 import Kitchen
elif index == 1:
    from utils_Kitchen_v1 import Kitchen
elif index == 2:
    from utils_Kitchen_v2 import Kitchen
else:
    assert False, "index should be 0, 1 or 2"

# pb_client = PbClient(enable_GUI=True, enable_Debug=True)
pb_client = PbClient(enable_GUI=False)
pb_client.enable_vertical_view(1.0, [2.3, 2.6, 2.3], -90, -75)
pb_visualizer = PbVisualizer(pb_client)
kitchen = Kitchen(pb_client)
print("object ids in loaded kitchen:\n{}".format(kitchen.object_ids))

# Get Object_Details such as:('Table', [1, 1, 0], [1.1020000000000003, 1.6520000000000001, 1.113], True)
# 其中object_details中存储的是Node的 name， position（仅代表在任意一轴的长度范围）， 具体的范围， 是否直接在地面上这四个属性 直接作用于后续Node2Vec的节点构建
# object_stacking中存储的是Node 的name， xyz轴的具体范围（如1.0-2.0），以及是否直接在地面上这四个属性，用于后续的给边写属性
object_details = []
object_stacking = []
for obj_name_id in kitchen.object_ids:
    obj_info = getattr(kitchen, obj_name_id)
    id, name, position = obj_info[0], obj_info[1], obj_info[2]
    ground_truth = pb_client.get_ground_truth(obj_info[0])
    obj_range = pb_client.get_bounding_box_xyz(obj_info[0])
    obj_special_range = pb_client.get_bounding_box(obj_info[0])
    object_details.append((name, position, obj_range, ground_truth))
    object_stacking.append((name, position, obj_special_range, ground_truth))
print("object_details is:", object_details)
print("object_stacking is:", object_stacking)
Edge_builder = EdgeBuilder(object_stacking)
Node_builder = NodeBuilder(object_details)
Edge_builder.edge_attribute_add()
# Edge_builder.build_edges()
Edge_builder.get_end_value()
Edge_builder.build_new_edges()
Edge_builder.normalize_and_weight_edges()
Node_builder.build_nodes()
edges = Edge_builder.get_edges()
nodes = Node_builder.get_nodes()
# # 这一部分是根据上述的nodes和edges构建Graph
Graph_Builder = GraphBuilder(nodes, edges)
Graph_Builder.build_Graph()
# plt.figure(figsize=(5, 5))  # 增大图形尺寸

# 绘制图
pos = nx.spring_layout(Graph_Builder.G)  # 或者使用其他布局
nx.draw(Graph_Builder.G, pos, with_labels=True, node_size=500, font_size=10)

# 如果需要，也可以单独绘制边的权重
labels = nx.get_edge_attributes(Graph_Builder.G, 'weight')
labels = {edge: format(weight, '.1f') for edge, weight in labels.items()}
nx.draw_networkx_edge_labels(Graph_Builder.G, pos, edge_labels=labels)

# plt.show()
walks = []
walk_length = 4  # 游走长度
cumulative_embeddings = {node: np.zeros(10) for node in Graph_Builder.G.nodes()}
num_iterations = 1000  # 总迭代次数
for _ in range(num_iterations):
    # 创建随机游走
    walks = []
    for node in Graph_Builder.G.nodes:
        walks.append(Graph_Builder.random_walk(node, walk_length))
    # walks = [Graph_Builder.random_walk('Bowl_Target', walk_length) for _ in range(len(nodes))]
    # 训练模型
    model = Word2Vec(walks, vector_size=10, window=2, min_count=2, sg=1)
    # 累积每个节点的嵌入向量
    for node in Graph_Builder.G.nodes():
        cumulative_embeddings[node] += model.wv[node]

# 计算平均嵌入向量
average_embeddings = {node: vec / num_iterations for node, vec in cumulative_embeddings.items()}
sorted_similarities = Sort_Similarity(average_embeddings)
for items in sorted_similarities:
    print(items)
pb_client.wait(10)
pb_client.disconnect_pybullet()