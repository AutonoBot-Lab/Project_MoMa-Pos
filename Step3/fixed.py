import math
import sys
import os
current_path = os.path.abspath(__file__)
utils_path = os.path.dirname(os.path.dirname(current_path)) + "/utils"
if os.path.basename(utils_path) != "utils":
    raise ValueError('Not add the path of folder "utils", please check again!')
sys.path.append(utils_path)
from utils.utils_Bestman import Bestman, Pose
from utils.utils_PbClient import PbClient
from utils.utils_PbVisualizer import PbVisualizer
#from utils.utils_Kitchen_object import Kitchen
import pybullet as p
"""
main functions
"""
# 第一部：找到base的高度
pb_client = PbClient(enable_GUI=True)
pb_client.enable_vertical_view(4.0, [1.0, 1.0, 0])
pb_visualizer = PbVisualizer(pb_client)
# logID = pb_client.start_record("example_manipulation") # start recording
init_pose = Pose([-2, -1, 0], [0.0, 0.0, math.pi / 2])
demo = Bestman(init_pose, pb_client) # load robot
demo.get_joint_link_info("arm") # get info about arm
init_joint = [0, -1.57, 2.0, -1.57, -1.57, 0]
demo.move_arm_to_joint_angles(init_joint) # reset arm joint position

# load table and bowl
table_id = pb_client.load_object(
    "./URDF_models/furniture_table_rectangle_high/table.urdf",
    [1.0, 1.0, 0.0],
    [0.0, 0.0, 0.0],
    1.0,
    "table",
    fixed_base=True,
)

# grasp target object
all_box_range=[]
num_joints = p.getNumJoints(table_id)
# pb_visualizer.draw_aabb_link(kitchen.elementE_id, num_joints-1)
for i in range(-1,num_joints):
    pb_visualizer.draw_aabb_link(table_id, i)
    range_links=pb_visualizer.draw_aabb_range(table_id, i)
    all_box_range.append(range_links)
    print(i,': num_joint range is:',range_links)
print('All boxes range are:',all_box_range)
pb_client.wait(100)
pb_client.disconnect_pybullet()