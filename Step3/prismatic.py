# 这段代码希望提取冰箱的结构信息，把所有的三维结构用坐标表示出来
import math
import sys
import os
import pybullet as p
import json
"""
Get the utils module path
"""
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
kitchen.open_it('elementC', 1)
num_joints = p.getNumJoints(kitchen.elementC_id)
# pb_visualizer.draw_aabb_link(kitchen.elementE_id, num_joints-1)
for i in range(0,num_joints):
    pb_visualizer.draw_aabb_link(kitchen.elementC_id, i)
    range_links=pb_visualizer.draw_aabb_range(kitchen.elementC_id, i)
    all_box_range.append(range_links)
    print(i,': num_joint range is:',range_links)
print('All boxes range are:',all_box_range)
pb_client.wait(100)
pb_client.disconnect_pybullet()
