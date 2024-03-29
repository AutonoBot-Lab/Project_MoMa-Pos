import math
import sys
import os
import pybullet as p
import time
import cProfile
import numpy as np
"""
Get the utils module path
调试：如果需要调试冰箱的情况，就把ob_id = 6，在kitchen_v2,H2改相应的坐标

"""
# customized package
current_path = os.path.abspath(__file__)
utils_path = os.path.dirname(os.path.dirname(current_path)) + '/utils'
if os.path.basename(utils_path) != 'utils':
    raise ValueError('Not add the path of folder "utils", please check again!')
sys.path.append(utils_path)
from utils_PbClient_moma_pos import PbClient
from utils_PbVisualizer_moma_pos import PbVisualizer
from utils_Parser import Parser
from utils_sample_R import Sample
from utils_Potential_R import Potential
from utils_Distance import Distance
from utils_OpenTSP import TSP
from utils_Bestman import Bestman, Pose
from utils_PbOMPL import PbOMPL
# load kitchen from three scenarios
index = 2
if index == 0:
    from utils_Kitchen_v0 import Kitchen
elif index == 1:
    from utils_Kitchen_v1 import Kitchen
elif index == 2:
    from utils_Kitchen_v2 import Kitchen
else:
    assert False, "index should be 0 or 1"
# 预先定义一些参数
object_details = []
object_stacking = []
ground_object = []
all_box_range = []
l1 = 0.4
l2 = 1.2
base_length = 0.85
display = False
target_3d_position = None
target_2d_position = None
init_pos = [2, 6, 0]

pb_client = PbClient(enable_GUI=False)
p.setGravity(0, 0, -9.8)
pb_client.enable_vertical_view(1, [1.7, 4.28, 1.95], -200, -52.3)
pb_visualizer = PbVisualizer(pb_client)

# 加载厨房环境
kitchen = Kitchen(pb_client)
kitchen.open_it("elementE", drawer_id=1, open_angle=math.pi / 2)
# print("object ids in loaded kitchen:\n{}".format(kitchen.object_ids))

# 加载机器人
init_pose = Pose(init_pos, [0.0, 0.0, math.pi / 2])
demo = Bestman(init_pose, pb_client)
demo.get_joint_link_info("arm")
init_joint = [0, -1.57, 2.0, -1.57, -1.57, 0]
demo.move_arm_to_joint_angles(init_joint)


Potential_map = [{(2.430679776858293, 1.6049292370883208): -1.9645008748445265}, {(2.725863607478579, 2.3461435910678543): -1.807504420096708}, {(2.7378368518372165, 2.1189509455847224): -1.8001565042014063}, {(2.743658673586897, 2.236317775660954): -1.7951220864468178}, {(2.5326055077233214, 1.5577722367758842): -1.7841692799179603}]

# 根据势能点信息，得到的Open Tsp路径
Distance_matrix = Distance(Potential_map, init_pos[:2])
Distance_matrix.cal_distance()
input_matrix = Distance_matrix.matrix
input_potential_map = Distance_matrix.potential_map
Tsp_route = TSP(input_matrix, input_potential_map)
best_route, points_route, elapsed_time_step3 = Tsp_route.Tsp_route()
print("Points route is:", points_route)
# 绘制路径图
Distance_matrix.draw_order_picture(best_route)
IK_time = 0
navigate_time = 0
# navigate
if not points_route:
    sucess = False
    threshold_distance = 0.1
    ompl = PbOMPL(
        pb_client=pb_client,
        arm_id=demo.arm_id,
        joint_idx=demo.arm_joint_indexs,
        tcp_link=demo.tcp_link,
        obstacles=[],
        planner="RRTConnect",
        threshold=threshold_distance,
    )
    ompl.add_scene_obstacles(display=False)
    ompl.check_obstacles()
    bowl_position = target_3d_position
    bowl_id = kitchen.elementH2_id[0]
    pb_client.run(100)
    _, _, min_z, _, _, max_z = pb_client.get_bounding_box(bowl_id)  # 注释掉了其中的print部分
    bowl_position[2] = max_z + demo.tcp_height * 1.5
    standing_orientation = [0.0, 0.0, math.pi / 2.0]
    standing_position = [init_pos[0], init_pos[1], 0]
    navigate_start_time = time.time()
    demo.navigate_base(Pose(standing_position, standing_orientation))  # 注释掉了其中的print部分
    navigate_end_time = time.time()
    navigate_time += (navigate_end_time - navigate_start_time)
    ompl.set_target(bowl_id)  # 注释掉了其中的print部分
    target_orientation = [0.0, math.pi / 2.0, 0.0]  # vertical
    goal = demo.cartesian_to_joints(position=bowl_position, orientation=target_orientation)
    IK_start_time = time.time()
    result = ompl.reach_object(start=demo.get_arm_joint_angle(), goal=goal,
                               end_effector_link_index=demo.end_effector_index)
    IK_end_time = time.time()
    IK_time += (IK_end_time - IK_start_time)


for next_position in points_route:
    sucess = False
    threshold_distance = 0.1
    ompl = PbOMPL(
        pb_client=pb_client,
        arm_id=demo.arm_id,
        joint_idx=demo.arm_joint_indexs,
        tcp_link=demo.tcp_link,
        obstacles=[],
        planner="RRTConnect",
        threshold=threshold_distance,
    )
    # add obstacles
    ompl.add_scene_obstacles(display=False)
    ompl.check_obstacles()

    bowl_position = target_3d_position
    bowl_id = kitchen.elementH2_id[0]
    pb_client.run(100)
    _, _, min_z, _, _, max_z = pb_client.get_bounding_box(bowl_id)  # 注释掉了其中的print部分
    bowl_position[2] = max_z + demo.tcp_height * 1.5
    standing_orientation = [0.0, 0.0, math.pi / 2.0]
    standing_position = [next_position[0], next_position[1], 0]
    navigate_start_time = time.time()
    demo.navigate_base(Pose(standing_position, standing_orientation))  # 注释掉了其中的print部分
    navigate_end_time = time.time()
    navigate_time += (navigate_end_time - navigate_start_time)
    ompl.set_target(bowl_id)  # 注释掉了其中的print部分
    target_orientation = [0.0, math.pi / 2.0, 0.0]  # vertical
    goal = demo.cartesian_to_joints(position=bowl_position, orientation=target_orientation)
    IK_start_time = time.time()
    result = ompl.reach_object(start=demo.get_arm_joint_angle(), goal=goal, end_effector_link_index=demo.end_effector_index)
    IK_end_time = time.time()
    IK_time += (IK_end_time - IK_start_time)
    if result[0] == True:
        sucess = True
        break
all_time = 0 + elapsed_time_step3
print("t1：", all_time)
print("t2：", IK_time)
print("t3：", navigate_time)
print("sucess:", sucess)
pb_client.wait(5)
pb_client.disconnect_pybullet()