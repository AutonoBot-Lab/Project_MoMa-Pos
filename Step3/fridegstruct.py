import math
import sys
import os
import pybullet as p
"""
Get the utils module path
"""

# 步骤
# 第一部：遍历三维场景中Element的所有link 第二部：在三维图像中构建势能网格 第三部：把三维的势能网格投影到二维的势能网格之中
# customized package cylinder_link=0.8+轮子的半径0.1=0.9
current_path = os.path.abspath(__file__)
utils_path = os.path.dirname(os.path.dirname(current_path)) + '/utils'
if os.path.basename(utils_path) != 'utils':
    raise ValueError('Not add the path of folder "utils", please check again!')
sys.path.append(utils_path)
from utils.utils_Bestman import Bestman, Pose
from utils.utils_PbClient import PbClient
from utils.utils_PbVisualizer import PbVisualizer
from utils.utils_PbOMPL import PbOMPL

# load kitchen from three scenarios
index = 0
if index == 0:
    from utils.utils_Kitchen_v0 import Kitchen
elif index == 1:
    from utils.utils_Kitchen_v1 import Kitchen
else:
    assert False, "index should be 0 or 1"


pb_client = PbClient(enable_GUI=True)
pb_client.enable_vertical_view(1.0, [1.7, 5.68, 1.95], -86.4, -52.3)
pb_visualizer = PbVisualizer(pb_client)
# logID = pb_client.start_record("example_manipulation") # start recording
init_pose = Pose([1, 0, 0], [0.0, 0.0, math.pi / 2])
demo = Bestman(init_pose, pb_client)  # load robot
demo.get_joint_link_info("arm")  # get info about arm
init_joint = [0, -1.57, 2.0, -1.57, -1.57, 0]
demo.move_arm_to_joint_angles(init_joint)  # reset arm joint position
all_box_range=[]
# load kitchen
kitchen = Kitchen(pb_client)
# pb_visualizer.draw_aabb_link(3, 0)
# print(type(kitchen.elementE_id))
print("object ids in loaded kitchen:\n{}".format(kitchen.object_ids))
object_in_kitchenB1B2=[kitchen.elementB1_id,kitchen.elementB2_id]
object_in_kitchenACDE=[kitchen.elementA_id,kitchen.elementC_id,kitchen.elementD_id,kitchen.elementE_id]
for kitchen_object in object_in_kitchenB1B2:
    num_joints = p.getNumJoints(kitchen_object)
    print(num_joints)
    pb_visualizer.draw_aabb_link(kitchen_object, -1)
    range1=pb_visualizer.draw_aabb_range(kitchen_object, -1)
    all_box_range.append(range1)

for kitchen_object1 in object_in_kitchenACDE:
    num_joints=p.getNumJoints(kitchen_object1)
    for i in range(num_joints):
        print(kitchen_object1,'  +  ',i)
        pb_visualizer.draw_aabb_link(kitchen_object1, i)
        range2=pb_visualizer.draw_aabb_range(kitchen_object1, i)
        all_box_range.append(range2)
        print('i num_joint range is:',range2)

print('All boxes range are:',all_box_range)
# # get occupancy grid
# occupancy_grid = pb_client.get_occupancy_network(demo.base_id)
# print('occupancy_grid:{}'.format(occupancy_grid))
# after open fridge
# kitchen.open_it('elementE', 1)
# pb_visualizer.draw_aabb_link(kitchen.elementE_id,0)
# # get occupancy grid
# occupancy_grid = pb_client.get_occupancy_network(demo.base_id, enable_plot=True)
# print('occupancy_grid:{}'.format(occupancy_grid))
# disconnect pybullet
pb_client.wait(100)
pb_client.disconnect_pybullet()