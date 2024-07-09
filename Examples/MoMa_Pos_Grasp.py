import os
import math
import sys
import pybullet as p
import time
import numpy as np
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目的根目录（假设 RoboticsToolBox 与 Examples 同级）
project_root = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from RoboticsToolBox import Bestman, Pose
from Env import Client_MoMa
from Visualization import Visualizer
from Motion_Planning.Manipulation import OMPL_Planner
from Motion_Planning.Navigation import *
from Utils import load_config
from MoMa_Utils import Distance, Sample, TSP, Potential, Parser

def main():
    # 定义机器人的相关参数
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
    bowl_id = 7

    # Load config
    config_path = '../Config/MoMa_Pos_Grasp.yaml'
    cfg = load_config(config_path)
    print(cfg)

    # Init client and visualizer
    client = Client_MoMa(cfg.Client)
    visualizer = Visualizer(client, cfg.Visualizer)

    # Load scene
    scene_path = '../Asset/Scene/MoMa_Kitchen.json'
    client.create_scene(scene_path)

    # Open fridge
    client.change_object_joint_angle("elementE", 1, math.pi / 2.0)

    # Init robot
    bestman = Bestman(client, visualizer, cfg)
    visualizer.change_robot_color(bestman.get_base_id(), bestman.get_arm_id(), False)

    # MoMa-Pos部分
    for obj_name_id in client.object_ids:
        obj_info = getattr(client, obj_name_id[1])
        id, name, position = obj_info[0], obj_info[1], obj_info[2]
        ground_truth = client.get_ground_truth(obj_info[0])
        if ground_truth == True:
            ground_object.append(id)
        if name == "Bowl_Target":
            target_3d_position = position
            target_2d_position = target_3d_position[:2]
        obj_range = client.get_bounding_box_xyz(obj_info[0])
        obj_special_range = client.get_bounding_box(obj_info[0])
        # obj_range代表了一个box的长宽高 obj_special_range表示一个box的六个角
        object_details.append((name, position, obj_range, ground_truth))
        object_stacking.append((name, position, obj_special_range, ground_truth))
    for item in ground_object:
        num_joints = p.getNumJoints(item)
        for i in range (-1, num_joints):
            range1 = visualizer.draw_aabb_range(item, i)
            all_box_range.append(range1)
    target_box_range = []
    # Assume that Bowl in Fridge
    ob_id = 6
    num_joints_target = p.getNumJoints(ob_id)
    for i in range (-1, num_joints_target):
        range2 = visualizer.draw_aabb_range(ob_id, i)
        target_box_range.append(range2)

    # 得到势能点,把势能点的信息存储在Potential_map中
    start_time_step2 = time.time()
    parser = Parser(all_box_range)
    obstacle_object_2d = parser.draw_xy()

    obstacle_object_2d = np.array(obstacle_object_2d)
    target_box_range = np.array(target_box_range)
    sample = Sample(target_2d_position, obstacle_object_2d, l1, l2, base_length)
    remaining_points = sample.generate_enough_points()

    potential = Potential(remaining_points, target_box_range, obstacle_object_2d, target_3d_position)
    potential.expand_with_z()

    Potential_map = potential.process_coordinates(display)
    end_time_step2 = time.time()
    elapsed_time_step2 = end_time_step2 - start_time_step2
    # print(f"step2代码执行时间：{elapsed_time_step2}秒")

    # 根据势能点信息，得到的Open Tsp路径
    Distance_matrix = Distance(Potential_map, bestman.init_pose.position[:2])
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

    # load OMPL planner
    ompl_planner = OMPL_Planner(
        bestman,
        cfg.Planner
    )

    # Get obstacles info
    ompl_planner.get_obstacles_info()



    # Navigation
    # standing_pose = Pose([3.1, 2.4, 0], [0.0, 0.0, 0.0])
    for next_position in points_route:
        sucess = False
        nav_planner = AStarPlanner(
            robot_size=bestman.get_robot_max_size(),
            obstacles_bounds=obstacle_object_2d,
            resolution=0.05,
            enable_plot=False
        )
        standing_orientation = [0.0, 0.0, math.pi / 2.0]
        standing_position = [next_position[0], next_position[1], 0]
        standing_pose = Pose(standing_position, standing_orientation)
        path = nav_planner.plan(bestman.get_current_base_pose(), standing_pose)
        bestman.navigate_base(standing_pose, path)

        # Init ompl planner
        ompl_planner = OMPL_Planner(
            bestman,
            cfg.Planner
        )

        # set target object for grasping
        ompl_planner.set_target(bowl_id)

        # reach target object
        result = ompl_planner.plan_execute()

        # grasp target object
        # bestman.sim_active_gripper(bowl_id, 1)

        if result[0] == True:
            sucess = True
            break

    # disconnect pybullet
    client.wait(10)
    client.disconnect()


if __name__ == '__main__':
    # set work dir to Examples
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()