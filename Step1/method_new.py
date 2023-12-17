# 这个方法和method.py不同点在与，把所有的类都叫做table，而不再分开考虑tables和bowls
from object import Table,Bowl,Checker
import torch
import numpy as np
def compute_distance(coord1, coord2):
    """Compute the Euclidean distance between two coordinates."""
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

class Transfor1:
    #构造方法是把所有的tables当作节点，并且传入所有的节点特征
    def __init__(self,tables):
        self.tables=tables
        self.nodes=self.tables
        self.table_features=[[table1.coordinates[0], table1.coordinates[1], table1.distance_to_length, table1.distance_to_width] for table1 in tables]
        self.node_features = [[node.coordinates[0], node.coordinates[1], node.distance_to_length, node.distance_to_width] for node in self.nodes]

    def x(self):
        features=self.table_features
        x1=torch.tensor(features , dtype=torch.float)
        return x1
    
    def edge_index(self):
        edge_matrix = []
        for i, table_base in enumerate(self.tables):
            for j, table_compared in enumerate(self.tables):
     #           if i != j:  # 避免将物体与自身进行比较
                    if Checker.whether_on_each_other(table_base, table_compared):
                        edge_matrix.append([j, i])
        return torch.tensor(edge_matrix).T

    def edge_index_distance(self):
        num_nodes = len(self.node_features)
        edge_matrix = []

        # Create edges for a fully connected graph
        for i in range(num_nodes):
            for j in range(num_nodes):
                    edge_matrix.append([i, j])

        return torch.tensor(edge_matrix, dtype=torch.long).t()
    
    def edge_weights_distance(self):
        nodes_weight = self.nodes
        edge_indices = []
        edge_weights = []
        for i, node1 in enumerate(nodes_weight):
            for j, node2 in enumerate(nodes_weight):
                distance = compute_distance(node1.coordinates, node2.coordinates)
                if distance == 0:  # handle self-loops by setting distance to infinity
                    edge_weights.append([float('inf')])
                else:
                    edge_weights.append([1 / distance])
                edge_indices.append([i, j])       
        edge_weights_distance= torch.tensor(edge_weights, dtype=torch.float)
        edge_weights_distance[edge_weights_distance== float('inf')] = 10
        edge_weights_distance=edge_weights_distance.squeeze()
        return edge_weights_distance