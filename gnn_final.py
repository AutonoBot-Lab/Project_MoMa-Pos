# 这段代码改进了网络参数
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv,GATConv
import torch_geometric.nn as pyg_nn
from torch_geometric.data import Data
from object import Table,Checker,Bowl
import numpy as np
from sklearn.metrics import f1_score, roc_curve, auc
import matplotlib.pyplot as plt
from torch_geometric.data import DataLoader
import torch_geometric.utils as pyg_utils
from method import Transfor
from method_new import Transfor1
import method
import pickle
import glob
import re
import pandas as pd
from torch.utils.data import random_split
from sklearn.metrics import precision_recall_fscore_support


def load_data(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)
#这个方法用于距离的计算
def compute_distance(coord1, coord2):
    """Compute the Euclidean distance between two coordinates."""
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

import torch_geometric.nn as pyg_nn

import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv

class WeightedDualEdgePredictor(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, alpha=0.7):
        super(WeightedDualEdgePredictor, self).__init__()
        
        # Mixing parameter
        self.alpha = alpha
        
        # Define the GCN convolution for edge_index_above
        self.conv1_above = GCNConv(in_channels, hidden_channels)      
        # Define the GAT convolution for edge_index_distance with edge_weights_distance
        self.conv1_distance = GATConv(in_channels, hidden_channels, heads=1)
        self.conv2_above = GCNConv(hidden_channels, hidden_channels)
        self.conv2_distance = GATConv(hidden_channels, hidden_channels, heads=1)
        self.conv3 = GCNConv(hidden_channels, hidden_channels)
        
        
        self.predictor = torch.nn.Sequential(
            torch.nn.Linear(2 * hidden_channels, hidden_channels),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_channels, 1),
            torch.nn.Sigmoid()
        )

    def forward(self, x, edge_index_above, edge_index_distance, edge_weights_distance):
        # Apply GCN for edge_index_above
        x_above_1= self.conv1_above(x, edge_index_above)
        # print("x_above.size:",x_above.size())
        x_above_1 = F.relu(x_above_1)
        
        # Apply GAT for edge_index_distance with edge_weights_distance
        x_distance_1 = self.conv1_distance(x, edge_index_distance, edge_weights_distance)
        x_distance_1 = F.relu(x_distance_1)

        x_above_2 = self.conv2_above(x_above_1, edge_index_above)
        x_above_2 = F.relu(x_above_2)

        x_distance_2 = self.conv2_distance(x_distance_1, edge_index_distance, edge_weights_distance)
        x_distance_2 = F.relu(x_distance_2)

        # Weighted combination of the outputs
        x_combined = self.alpha * x_above_2 + (1 - self.alpha) * x_distance_2
        
        # Further node update using GCN
        x = self.conv3(x_combined, edge_index_above)  # We are using edge_index_above here, adjust if needed
        x = F.relu(x)
        
        # Predicting edges
        all_possible_edges = torch.cartesian_prod(torch.arange(x.size(0), device=x.device), torch.arange(x.size(0), device=x.device)).t() 
        start_features = x[all_possible_edges[0]]
        end_features = x[all_possible_edges[1]]
        edge_features = torch.cat([start_features, end_features], dim=1)

        return self.predictor(edge_features).squeeze(-1)

#--------------训练数据
table_graph=[]
folder_path_graph = '/home/shaobeichen/robot/BestMan-step3/BestMan_Pybullet-master/examples/GNN/train/table_graph'  # graph
# 使用 glob 模块找到文件夹中所有的 .csv 文件
csv_files = glob.glob(f"{folder_path_graph}/graph*.csv")
# 按文件名中的数字排序
csv_files.sort(key=lambda x: int(re.search(r'graph(\d+)\.csv', x).group(1)))
# 初始化一个列表来存储张量
for graph_file in csv_files:
    graph_data = pd.read_csv(graph_file)
    data_tran=[] #这个data_tran是用来存储tabel_graph中每一个包含多个table的元素
#   print(graph_data)
    for index, row in graph_data.iterrows():
        table_current=Table(
            coordinates=(row['center1'],row['center2']),
            distance_to_length=row['distance_to_length'],
            distance_to_width=row['distance_to_width']
        )
        data_tran.append(table_current)
    table_graph.append(data_tran)
#定义label--------------------------------------------------
folder_path = '/home/shaobeichen/robot/BestMan-step3/BestMan_Pybullet-master/examples/GNN/train/table_label'  # label
# 使用 glob 模块找到文件夹中所有的 .csv 文件
csv_files = glob.glob(f"{folder_path}/label*.csv")
# 按文件名中的数字排序
csv_files.sort(key=lambda x: int(re.search(r'label(\d+)\.csv', x).group(1)))
# 初始化一个列表来存储张量
tensors_list = []
# 遍历找到的所有 .csv 文件
for file in csv_files:
    # 读取 CSV 文件
    data = pd.read_csv(file)
    # 将 DataFrame 数据转换为一维 NumPy 数组
    flattened_data = data.values.flatten()  
    # 转换为 PyTorch 张量并存储到列表中
    tensor = torch.tensor(flattened_data, dtype=torch.float32)
    tensors_list.append(tensor)
# #---------------------------------------all_graphs_tables_str为所有graph的值为[]
data_list = []  # 初始化 data_list 为空列表

# 遍历 table_graph 和 tensors_list
for table_per, tensor_per in zip(table_graph, tensors_list):
    transform = Transfor1(table_per)  # 使用 Transfor1 处理当前的 table 数据
    # 创建 Data 对象
    data_per = Data(
        x=transform.x(),
        edge_index_above=transform.edge_index(),
        edge_index_distance=transform.edge_index_distance(),
        edge_weights_distance=transform.edge_weights_distance(),
        y=tensor_per  # 从 tensors_list 获取当前的 y 值
    )
    # 将 Data 对象添加到 data_list 中
    data_list.append(data_per)
#--------------训练数据
 # 您的所有图数据
total_size = len(data_list)
train_size = int(total_size * 0.8)
val_size = int(total_size * 0.1)
test_size = total_size - train_size - val_size 
# 分割数据集
train_dataset, val_dataset, test_dataset = random_split(data_list, [train_size, val_size, test_size])

# 创建不同的数据加载器
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)
# 1. 初始化模型和优化器
# 定义模型、损失函数和优化器
hidden_channels=64
# print("tezheng:",data.x.size(1)) data1.x.size(1)
model = WeightedDualEdgePredictor(4, hidden_channels)
criterion = torch.nn.BCELoss()  # 二元交叉熵损失函数
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
train_losses = []
val_losses = []

# 训练模型
epochs = 200
for epoch in range(epochs):
    model.train()
    total_train_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        out = model(batch.x, batch.edge_index_above, batch.edge_index_distance, batch.edge_weights_distance)
        loss = criterion(out, batch.y.float())
        loss.backward()
        optimizer.step()
        total_train_loss += loss.item()
    
    # 记录训练损失
    avg_train_loss = total_train_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # 执行验证
    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            out = model(batch.x, batch.edge_index_above, batch.edge_index_distance, batch.edge_weights_distance)
            loss = criterion(out, batch.y.float())
            total_val_loss += loss.item()
    
    # 记录验证损失
    avg_val_loss = total_val_loss / len(val_loader)
    val_losses.append(avg_val_loss)

    # 打印进度
    print(f"Epoch {epoch+1}/{epochs}, Training Loss: {avg_train_loss}, Validation Loss: {avg_val_loss}")

# # 绘制训练和验证损失
# plt.plot(train_losses, label='Training Loss')
# plt.plot(val_losses, label='Validation Loss')
# plt.title('Training and Validation Loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()

# 测试模型
model.eval()
y_true = []
y_pred = []
with torch.no_grad():
    for batch in test_loader:
        out = model(batch.x, batch.edge_index_above, batch.edge_index_distance, batch.edge_weights_distance)
        preds = (out > 0.5).float()  # 预测阈值设置为0.5
        y_true.extend(batch.y.view(-1).cpu().numpy())
        y_pred.extend(preds.view(-1).cpu().numpy())

# 计算并打印性能指标
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')

# 保存模型
# torch.save(model.state_dict(), '/mnt/data/model.pth')