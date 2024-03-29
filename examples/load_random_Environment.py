import math
import sys
import os
import pybullet as p

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
# load kitchen from three scenarios
index = 2
if index == 0:
    from utils_Kitchen_v0 import Kitchen
elif index == 1:
    from utils_Kitchen_v1 import Kitchen
elif index == 2:
    from utils_random_kitchen import Kitchen
else:
    assert False, "index should be 0 or 1"

pb_client = PbClient(enable_GUI=True)
p.setGravity(0, 0, -9.8)
pb_client.enable_vertical_view(2.2, [1.9, -0.35, 1.54], yaw=-88, pitch=-31.5)
pb_visualizer = PbVisualizer(pb_client)

kitchen = Kitchen(pb_client)
print("object ids in loaded kitchen:\n{}".format(kitchen.object_ids))

# Get Object_Details such as:('Table', [1, 1, 0], [1.1020000000000003, 1.6520000000000001, 1.113], True)
# 其中object_details中存储的是Node的 name， position（仅代表在任意一轴的长度范围）， 具体的范围， 是否直接在地面上这四个属性 直接作用于后续Node2Vec的节点构建
# object_stacking中存储的是Node 的name， xyz轴的具体范围（如1.0-2.0），以及是否直接在地面上这四个属性，用于后续的给边写属性
object_details = []
object_stacking= []
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

pb_client.wait(10)
pb_client.disconnect_pybullet()