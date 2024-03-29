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
# [2, 6, 0]
init_pos = [2, 6, 0]

kitchen_start_time = time.time()
pb_client = PbClient(enable_GUI=True)
p.setGravity(0, 0, -9.8)
# Table_normal:4, [2, 3.28, 2], 0, 0
# Table_TopDown:3, [2, 2.28, 1]
# Drawer_TopDown:4, [3.6, 2.4,1]
# Fridge_3_TopDown:2, [4, 5.3, 2]
# Fridge_2_TopDown:2, [4, 5.3, 2]
pb_client.enable_vertical_view(4, [2, 2.4,2],0 , 0)
pb_visualizer = PbVisualizer(pb_client)

# 加载厨房环境

kitchen = Kitchen(pb_client)
kitchen_end_time = time.time()
kitchen_time = kitchen_end_time - kitchen_start_time
# 打开Fridge
# kitchen.open_it("elementE", drawer_id=1, open_angle=math.pi / 2)
# 打开Dishwash
# kitchen.open_it("elementC", drawer_id=1, open_angle=math.pi / 2)
# print("object ids in loaded kitchen:\n{}".format(kitchen.object_ids))

# 加载机器人
init_pose = Pose(init_pos, [0.0, 0.0, math.pi / 2])
demo = Bestman(init_pose, pb_client)
demo.get_joint_link_info("arm")
init_joint = [0, -1.57, 2.0, -1.57, -1.57, 0]
demo.move_arm_to_joint_angles(init_joint)

# 从环境中获取后续所需的关键参数，如二维的结构
for obj_name_id in kitchen.object_ids:
    obj_info = getattr(kitchen, obj_name_id)
    id, name, position = obj_info[0], obj_info[1], obj_info[2]
    ground_truth = pb_client.get_ground_truth(obj_info[0])
    if ground_truth == True:
        ground_object.append(id)
    if name == "Bowl_Target":
        target_3d_position = position
        target_2d_position = target_3d_position[:2]
    obj_range = pb_client.get_bounding_box_xyz(obj_info[0])
    obj_special_range = pb_client.get_bounding_box(obj_info[0])
    object_details.append((name, position, obj_range, ground_truth))
    object_stacking.append((name, position, obj_special_range, ground_truth))

for item in ground_object:
    num_joints = p.getNumJoints(item)
    for i in range(-1, num_joints):
        range1 = pb_visualizer.draw_aabb_range(item, i)
        all_box_range.append(range1)

target_box_range = []
# ob_id = 6: Fridge ; ob_id = 7:Table ; ob_id = 1 drawer; ob_id = 2 B1; ob_id = 3 B2;ob_id = 4 Dishwash
ob_id = 1
num_joints_target = p.getNumJoints(ob_id)
for i in range(-1, num_joints_target):
    range2 = pb_visualizer.draw_aabb_range(ob_id, i)
    target_box_range.append(range2)

# 得到势能点,把势能点的信息存储在Potential_map中
start_time_step2 = time.time()
Parser = Parser(all_box_range)
obstacle_object_2d = Parser.draw_xy()


obstacle_object_2d = np.array(obstacle_object_2d)
target_box_range = np.array(target_box_range)
Sample = Sample(target_2d_position, obstacle_object_2d, l1, l2, base_length)
remaining_points = Sample.generate_enough_points()

Potential = Potential(remaining_points, target_box_range, obstacle_object_2d, target_3d_position)
Potential.expand_with_z()

Potential_map = Potential.process_coordinates(display)
end_time_step2 = time.time()
elapsed_time_step2 = end_time_step2 - start_time_step2
# print(f"step2代码执行时间：{elapsed_time_step2}秒")

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
# 开始录制，视频文件名为'my_simulation'
log_id = pb_client.start_record('test_Drawer_2_Nor')
pb_client.wait(10)
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
    standing_orientation = [0.0, 0.0, -math.pi / 2.0]
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
all_time = elapsed_time_step2 + elapsed_time_step3
pb_client.wait(10)
pb_client.end_record(log_id)
print("t1：", all_time)
print("t2：", IK_time)
print("t3：", navigate_time)
print("sucess:", sucess)
pb_client.wait(5)
pb_client.disconnect_pybullet()