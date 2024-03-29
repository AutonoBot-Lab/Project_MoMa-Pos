import pybullet as p
import pybullet_data
import math
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

"""
Get the utils module path
"""
import sys
import os

# customized package
current_path = os.path.abspath(__file__)
utils_path = os.path.dirname(current_path)
if os.path.basename(utils_path) != "utils":
    raise ValueError('Not add the path of folder "utils", please check again!')
sys.path.append(utils_path)
from utils_PbVisualizer_moma_pos import PbVisualizer
from utils_PbClient_moma_pos import PbClient

# from utils_PIDController import PIDController

"""
Add kitchen
"""


class Kitchen:
    def __init__(self, pb_client):
        self.pb_client = pb_client
        self.client_id = self.pb_client.get_client()

        self.object_ids = []  # store object id in loaded kitchen scene

        # ----------------------------------------------------------------
        # This is Element F (i.e., a table)
        # ----------------------------------------------------------------
        self.elementF_id = self.pb_client.load_object(
            # model_path="./URDF_models/furniture_table_rectangle_high_nocolor/table.urdf",
            model_path="./URDF_models/furniture_table_rectangle_high/table.urdf",
            object_position=[1.5, 2, 0],
            object_orientation=[0, 0, math.pi / 2.0],
            scale=1,
            obj_name="elementF",
            fixed_base=True,
        )
        self.object_ids.append("elementF_id")

        # ----------------------------------------------------------------
        # This is Element G1 (i.e., chairs)
        # ----------------------------------------------------------------
        # self.elementG1_id = self.pb_client.load_object(
        #     model_path="./URDF_models/furniture_chair/model.urdf",
        #     object_position=[1.5, 2.8, 0],
        #     object_orientation=[math.pi / 2.0 * 3, 0.0, math.pi * 1.5],
        #     scale=1,
        #     obj_name="elementG1",
        #     fixed_base=True,
        # )
        # self.object_ids.append("elementG1_id")
        #
        # self.elementG2_id = self.pb_client.load_object(
        #     model_path="./URDF_models/furniture_chair/model.urdf",
        #     object_position=[2.1, 2.2, 0],
        #     object_orientation=[math.pi / 2.0 * 3, 0.0, math.pi],
        #     scale=1,
        #     obj_name="elementG2",
        #     fixed_base=True,
        # )
        # self.object_ids.append("elementG2_id")
        #
        # self.elementG3_id = self.pb_client.load_object(
        #     model_path="./URDF_models/furniture_chair/model.urdf",
        #     object_position=[1.5, 1.1, 0],
        #     object_orientation=[math.pi / 2.0 * 3, 0.0, math.pi / 2.0],
        #     scale=1,
        #     obj_name="elementG3",
        #     fixed_base=True,
        # )
        # self.object_ids.append("elementG3_id")
        #
        # self.elementG4_id = self.pb_client.load_object(
        #     model_path="./URDF_models/furniture_chair/model.urdf",
        #     object_position=[2.1, 2.7, 0],
        #     object_orientation=[math.pi / 2.0 * 3, 0.0, math.pi],
        #     scale=1,
        #     obj_name="elementG4",
        #     fixed_base=True,
        # )
        # self.object_ids.append("elementG4_id")

        # ----------------------------------------------------------------
        # This is Element H (i.e., small objects)
        # ----------------------------------------------------------------

        self.elementH2_id = self.pb_client.load_object(
            # model_path="./URDF_models/bowl/model.urdf",
            model_path="./URDF_models/utensil_bowl_blue/model.urdf",
            # [4, 5.3, 1.368] fridge
            # [1.7, 2.2, 0.85] table
            # [3.6, 2.4, 0.9] drawer
            # [4, 4, 1.0] B1
            # [4.1, 4.5, 1] B2
            object_position=[1.7, 2.2, 1],
            object_orientation=[0, 0, 0],
            scale=1.1,
            obj_name="Bowl_Target",
            fixed_base=False,
        )
        self.object_ids.append("elementH2_id")




        # ----------------------------------------------------------------
        # Set element A B C D E colors
        # ----------------------------------------------------------------
        self.visualizer = PbVisualizer(pb_client)
        self.visualizer.set_elementF_visual_color(self.elementF_id[0])
        # self.visualizer.set_elementG_visual_color(self.elementG1_id[0])
        # self.visualizer.set_elementG_visual_color(self.elementG2_id[0])
        # self.visualizer.set_elementG_visual_color(self.elementG3_id[0])
        # self.visualizer.set_elementG_visual_color(self.elementG4_id[0])

    # ----------------------------------------------------------------
    # Open drawer
    # ----------------------------------------------------------------
    def open_it(self, elementName, drawer_id, open_angle=None):
        if elementName == "elementA":
            joint_id = self.elementA_drawer_to_joint_id[drawer_id]
            if open_angle is None:
                open_angle = self.elementA_drawer_to_joint_limits[drawer_id][1]
            # print("elementA: joint_id:{}, open_angle:{}".format(joint_id, open_angle))
            p.setJointMotorControl2(
                bodyIndex=self.elementA_id[0],
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=open_angle,
                maxVelocity=1.0,
            )
        elif elementName == "elementC":
            joint_id = self.elementC_drawer_to_joint_id[drawer_id]
            if open_angle is None:
                open_angle = self.elementC_drawer_to_joint_limits[drawer_id][1]
            # print("elementC: joint_id:{}, open_angle:{}".format(joint_id, open_angle))
            p.setJointMotorControl2(
                bodyIndex=self.elementC_id[0],
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=open_angle,
                maxVelocity=1.0,
            )
        elif elementName == "elementD":
            joint_id = self.elementD_drawer_to_joint_id[drawer_id]
            if open_angle is None:
                open_angle = self.elementD_drawer_to_joint_limits[drawer_id][1]
            # print(
            #     "elementD (open): joint_id:{}, open_angle:{}".format(
            #         joint_id, open_angle
            #     )
            # )
            p.setJointMotorControl2(
                bodyIndex=self.elementD_id[0],
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=open_angle,
                maxVelocity=1.0,
            )
        elif elementName == "elementE":
            joint_id = self.elementE_drawer_to_joint_id[drawer_id]
            if open_angle is None:
                open_angle = self.elementE_drawer_to_joint_limits[drawer_id][1]
            # print("elementE: joint_id:{}, open_angle:{}".format(joint_id, open_angle))
            p.setJointMotorControl2(
                bodyIndex=self.elementE_id[0],
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=open_angle,
                maxVelocity=1.0,
            )
        self.pb_client.run(240 * 5)

    # ----------------------------------------------------------------
    # Close drawer
    # ----------------------------------------------------------------
    def close_it(self, elementName, drawer_id, open_angle=None):
        if elementName == "elementA":
            joint_id = self.elementA_drawer_to_joint_id[drawer_id]
            close_angle = self.elementA_drawer_to_joint_limits[drawer_id][0]
            p.setJointMotorControl2(
                bodyIndex=self.elementA_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=close_angle,
                maxVelocity=1.0,
            )
        elif elementName == "elementC":
            joint_id = self.elementC_drawer_to_joint_id[drawer_id]
            close_angle = self.elementC_drawer_to_joint_limits[drawer_id][0]
            p.setJointMotorControl2(
                bodyIndex=self.elementC_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=close_angle,
                maxVelocity=1.0,
            )
            self.pb_client.run(240 * 5)

        elif elementName == "elementD":
            joint_id = self.elementD_drawer_to_joint_id[drawer_id]
            close_angle = self.elementD_drawer_to_joint_limits[drawer_id][0]
            # print(
            #     "elementD (close): joint_id:{}, open_angle:{}".format(
            #         joint_id, close_angle
            #     )
            # )
            p.setJointMotorControl2(
                bodyIndex=self.elementD_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=close_angle,
                maxVelocity=1.0,
            )
        elif elementName == "elementE":
            joint_id = self.elementE_drawer_to_joint_id[drawer_id]
            close_angle = self.elementE_drawer_to_joint_limits[drawer_id][0]
            p.setJointMotorControl2(
                bodyIndex=self.elementE_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=close_angle,
                maxVelocity=1.0,
            )
        self.pb_client.run(240)
