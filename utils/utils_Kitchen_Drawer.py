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
        self.elementA_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models_yan/elementA/urdf/kitchen_part_right_gen_convex.urdf",
            object_position=[4, 2, 1.477],
            object_orientation=[0, 0, math.pi],
            scale=1.0,
            obj_name="elementA",
            fixed_base=True,
        )
        self.object_ids.append("elementA_id")
        self.elementA_drawer_to_joint_id = {
            1: 17,
            2: 21,
            3: 26,
            4: 30,
            5: 36,
            6: 39,
            7: 47,
            8: 52,
            9: 55,
            10: 57,
            11: 13,
        }
        self.elementA_drawer_to_joint_limits = {
            1: (0, math.pi / 2.0),
            4: (0, math.pi / 2.0),
            7: (0, math.pi / 2.0),
            5: (0.0, 0.4),
            6: (0.0, 0.4),
            9: (0.0, 0.4),
            10: (0.0, 0.4),
            11: (0, math.pi / 2.0),
            2: (0, -math.pi / 2.0),
            3: (0, -math.pi / 2.0),
            8: (0, -math.pi / 2.0),
        }

        self.open_it("elementA", drawer_id=5)
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

        self.elementH2_id = self.pb_client.load_object(
            # model_path="./URDF_models/bowl/model.urdf",
            model_path="./URDF_models/utensil_bowl_blue/model.urdf",
            # [4, 5.3, 1.368] fridge
            # [1.7, 2.2, 0.85] table
            # [3.6, 2.4, 0.9] drawer
            # [4, 4, 1.0] B1
            # [4.1, 4.5, 1] B2
            object_position=[3.6, 2.4, 0.9],
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
        self.visualizer.set_elementA_visual_color(self.elementA_id[0])
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
