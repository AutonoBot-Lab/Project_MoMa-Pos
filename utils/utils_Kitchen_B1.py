"""
@Description :   kitchen 2
@Author      :   Yan Ding
@Time        :   2024/01/07 16:51:36
"""

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
        # This is Element A, where there are a oven, and a few drawers
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        self.elementB1_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models_yan/elementB/model.urdf",
            object_position=[4.1, 4.55, 0.55],
            object_orientation=[0, 0, math.pi / 2 * 3],
            scale=1.1,
            obj_name="elementB1",
            fixed_base=True,
        )
        self.object_ids.append("elementB1_id")

        self.elementB2_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models_yan/elementB/model.urdf",
            object_position=[4.1, 5.25, 0.55],
            object_orientation=[0, 0, math.pi / 2 * 3],
            scale=1.1,
            obj_name="elementB2",
            fixed_base=True,
        )
        self.object_ids.append("elementB2_id")

        # ----------------------------------------------------------------
        #  This is Element C (i.e., a dishwasher)
        # ----------------------------------------------------------------
        self.elementC_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models/Dishwasher/2085/mobility.urdf",
            object_position=[3.85, 3.2, 0.35],
            object_orientation=[0, 0, 0],
            scale=0.75,
            obj_name="elementC",
            fixed_base=True,
        )
        self.object_ids.append("elementC_id")
        self.elementC_drawer_to_joint_id = {
            1: 1,
        }
        self.elementC_drawer_to_joint_limits = {
            1: (0, math.pi / 2.0),
        }
        # self.open_it("elementC", drawer_id=1, open_angle=math.pi/2)
        # print(
        #     "-" * 20
        #     + "\n"
        #     + "Element C's drawer id in kithen: {}".format(
        #         self.elementC_drawer_to_joint_id
        #     )
        # )

        # ----------------------------------------------------------------
        # This is Element D (i.e., a microwave)
        # ----------------------------------------------------------------

        self.elementH2_id = self.pb_client.load_object(
            # model_path="./URDF_models/bowl/model.urdf",
            model_path="./URDF_models/utensil_bowl_blue/model.urdf",
            # [4, 5.3, 1.368] fridge
            # [1.7, 2.2, 0.85] table
            # [3.6, 2.4, 0.9] drawer
            # [4, 4, 1.0] B1
            # [4.1, 4.5, 1] B2
            object_position=[4, 4, 1],
            object_orientation=[0, 0, 0],
            scale=1.1,
            obj_name="Bowl_Target",
            fixed_base=False,
        )
        self.object_ids.append("elementH2_id")



        self.elementH7_id = self.pb_client.load_object(
            model_path="./URDF_models/mug/model.urdf",
            object_position=[3.9, 4.6, 1.0],
            object_orientation=[0, 0, 0],
            scale=1.3,
            obj_name="mug",
            fixed_base=False,
        )
        self.object_ids.append("elementH7_id")

        self.elementH8_id = self.pb_client.load_object(
            model_path="./URDF_models/toothpaste_1/model.urdf",
            object_position=[3.9, 4.9, 1.0],
            object_orientation=[math.pi, 0, 0],
            scale=1.0,
            obj_name="toothpaste_1",
            fixed_base=False,
        )
        self.object_ids.append("elementH8_id")



        # ----------------------------------------------------------------
        # Set element A B C D E colors
        # ----------------------------------------------------------------
        self.visualizer = PbVisualizer(pb_client)
        self.visualizer.set_elementB_visual_color(self.elementB1_id[0])
        self.visualizer.set_elementB_visual_color(self.elementB2_id[0])
        self.visualizer.set_elementC_visual_color(self.elementC_id[0])


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
