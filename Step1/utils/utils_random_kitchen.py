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
if os.path.basename(utils_path) != 'utils':
    raise ValueError('Not add the path of folder "utils", please check again!')
sys.path.append(utils_path)
from utils_PbVisualizer import PbVisualizer
from utils_PbClient import PbClient
# from utils_PIDController import PIDController

"""
Add kitchen
"""

class Kitchen:
    # Environment elementA-I 

    def __init__(self, pb_client):
        self.pb_client = pb_client
        self.client_id = self.pb_client.get_client()
        
        self.object_ids = [] # store object id in loaded kitchen scene
   
        self.elementA_id = self.pb_client.load_object(
            model_path = "./URDF_models/furniture_table_rectangle_high/table.urdf",
            object_position = [1,1,0],
            #object_position = [round(random.uniform(-5, 5), 2),round(random.uniform(-5, 5), 2),0],
            object_orientation = [0,0,math.pi / 2.0],
            scale=1.1,
            obj_name='Table',
            fixed_base=False,
        )

        self.object_ids.append("elementA_id")

        self.elementB_id = self.pb_client.load_object(
            model_path = "./URDF_models/furniture_chair/model.urdf",
            object_position = [1,3,0],
            # object_position = [round(random.uniform(-5, 5), 2),round(random.uniform(-5, 5), 2),0],
            object_orientation = [math.pi / 2.0 * 3, 0.0, math.pi * 1.5],
            scale=1.5,
            obj_name='Chair_A',
            fixed_base=False,
        )
        self.object_ids.append("elementB_id")

        self.elementC_id = self.pb_client.load_object(
            model_path = "./URDF_models/furniture_chair/model.urdf",
            object_position = [2.5,1,0],
            # object_position = [round(random.uniform(-5, 5), 2),round(random.uniform(-5, 5), 2),0],
            object_orientation = [math.pi / 2.0 * 3, 0.0, math.pi ],
            scale=1.5,
            obj_name='Chair_B',
            fixed_base=False,
        )
        self.object_ids.append("elementC_id")

        self.elementC1_id = self.pb_client.load_object(
            model_path = "./URDF_models/furniture_chair/model.urdf",
            object_position = [1,-1,0],
            # object_position = [round(random.uniform(-5, 5), 2),round(random.uniform(-5, 5), 2),0],
            object_orientation = [math.pi / 2.0 * 3, 0.0, math.pi / 2.0 ],
            scale=1.5,
            obj_name='Chair_C',
            fixed_base=False,
        )
        self.object_ids.append("elementC1_id")

        self.elementD_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models_yan/elementA/urdf/kitchen_part_right_gen_convex.urdf",
            object_position=[4, 2, 1.477],
            object_orientation=[0, 0, math.pi],
            scale=1.0,
            obj_name='Convex',
            fixed_base=True,
        )
        self.object_ids.append("elementD_id")
        self.elementD_drawer_to_joint_id = {
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
        self.elementD_drawer_to_joint_limits = {
            1: (0, math.pi/2.0),
            4: (0, math.pi/2.0),
            7: (0, math.pi/2.0),
            5: (0.0, 0.4),
            6: (0.0, 0.4),
            9: (0.0, 0.4),
            10: (0.0, 0.4),
            11: (0, math.pi/2.0),
            2: (0, -math.pi/2.0),
            3: (0, -math.pi/2.0),
            8: (0, -math.pi/2.0),
        }
        print(
            "-" * 20
            + "\n"
            + "Element D's drawer id in kithen: {}".format(
                self.elementD_drawer_to_joint_id
            )
        )

        self.elementE_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models/Fridge/10144/mobility.urdf",
            # object_position=[4.1, 4, 1.055],
            object_position = [4.1, 5.42,1.055],
            object_orientation=[0, 0, 0],
            scale=1.1,
            obj_name='Fridge',
            fixed_base=False,
        )
        self.object_ids.append("elementE_id")
        self.elementE_drawer_to_joint_id = {
            1: 1
        }
        self.elementE_drawer_to_joint_limits = {
            1: (0, math.pi/2.0),
        }
        print(
            "-" * 20
            + "\n"
            + "Element E's drawer id in kithen: {}".format(
                self.elementE_drawer_to_joint_id
            )
        )
        self.elementF_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models_yan/elementB/model.urdf",
            object_position=[4.1, 4.55, 0.55],
            object_orientation=[0, 0, math.pi/2*3],
            scale=1.1,
            obj_name='elementF',
            fixed_base=True,
        )
        self.object_ids.append("elementF_id")

        self.elementG_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models_yan/elementB/model.urdf",
            object_position=[4.1, 5.25, 0.55],
            object_orientation=[0, 0, math.pi/2*3],
            scale=1.1,
            obj_name='elementG',
            fixed_base=True,
        )
        self.object_ids.append("elementG_id")

        self.elementH_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models/Dishwasher/2085/mobility.urdf",
            object_position=[3.85, 3.2, 0.35],
            object_orientation=[0, 0, 0],
            scale=0.75,
            obj_name='Dishwasher',
            fixed_base=True,
        )
        self.object_ids.append("elementH_id")
        self.elementH_drawer_to_joint_id = {
            1: 1,
        }
        self.elementH_drawer_to_joint_limits = {
            1: (0, math.pi/2.0),
        }
        print(
            "-" * 20
            + "\n"
            + "Element H's drawer id in kithen: {}".format(
                self.elementH_drawer_to_joint_id
            )
        )

        self.elementI_id = self.pb_client.load_object(
            model_path="./Kitchen_models/models/Microwave/7128/mobility.urdf",
            object_position=[4.0, 2.9, 1.1],
            object_orientation=[0, 0, 0],
            scale=0.5,
            obj_name='Microwave',
            fixed_base=True,
        )
        self.object_ids.append("elementI_id")
        self.elementI_drawer_to_joint_id = {
            1: 1,
        }
        self.elementI_drawer_to_joint_limits = {
            1: (0, math.pi/2.0),
        }
        print(
            "-" * 20
            + "\n"
            + "Element I's drawer id in kithen: {}".format(
                self.elementI_drawer_to_joint_id
            )
        )

        # ----------------------------------------------------------------
        # Target Random Table
        # ----------------------------------------------------------------
        self.elementJ_id = self.pb_client.load_object(
            model_path = "./URDF_models/food_peach/model.urdf",
            object_position = [0.8,0.5,0.9],
            #object_position = [round(random.uniform(0.5, 1.5), 3),round(random.uniform(0.2, 1.8), 3),0.90],
            object_orientation = [0,0,math.pi ],
            scale=1.1,
            obj_name='Peach',
            fixed_base=False,
        )
        self.object_ids.append("elementJ_id")

        self.elementK_id = self.pb_client.load_object(
            model_path = "./URDF_models/bowl/model.urdf",
            object_position = [0.7,1.0,0.97],
            #object_position = [round(random.uniform(0.5, 1.5), 3),round(random.uniform(0.2, 1.8), 3),0.94],
            object_orientation = [0,0,math.pi ],
            scale=1.1,
            obj_name='Bowl_Target',
            fixed_base=False,
        )
        self.object_ids.append("elementK_id")

        self.elementL_id = self.pb_client.load_object(
            model_path = "./URDF_models/food_banana/model.urdf",
            object_position = [0.6,0.6,0.9],
            # object_position = [round(random.uniform(0.5, 1.5), 3),round(random.uniform(0.2, 1.8), 3),0.90],
            object_orientation = [0,0,math.pi],
            scale=1.0,
            obj_name='Banana',
            fixed_base=False,
        )
        self.object_ids.append("elementL_id")

        self.elementM_id = self.pb_client.load_object(
            model_path = "./URDF_models/food_bread/model.urdf",
            object_position = [0.7,0.7,0.9],
            # object_position = [round(random.uniform(0.5, 1.5), 3),round(random.uniform(0.2, 1.8), 3),0.90],
            object_orientation = [0,0,0],
            scale=1.0,
            obj_name='Bread',
            fixed_base=False,
        )
        self.object_ids.append("elementM_id")

        self.elementN_id = self.pb_client.load_object(
            model_path = "./URDF_models/food_lemon/model.urdf",
            object_position = [0.8,0.8,0.9],
            #object_position = [round(random.uniform(0.5, 1.5), 3),round(random.uniform(0.2, 1.8), 3),0.90],
            object_orientation = [0,0,0 ],
            scale=1.0,
            obj_name='Lemon',
            fixed_base=False,
        )
        self.object_ids.append("elementN_id")
        # ----------------------------------------------------------------
        # Target Random Outside Table
        # ----------------------------------------------------------------
        self.elementO_id = self.pb_client.load_object(
            model_path = "./URDF_models/book_2/model.urdf",
            object_position = [3.9,4.6,1.0],
            # object_position = [round(random.uniform(3.8, 4.4), 3),round(random.uniform(4.4, 5.0), 3),1.0],
            object_orientation = [0,0,0 ],
            scale=1.0,
            obj_name='Book_A',
            fixed_base=False,
        )
        self.object_ids.append("elementO_id")

        self.elementP_id = self.pb_client.load_object(
            model_path = "./URDF_models/book_2/model.urdf",
            object_position = [3.9,4.9,1.0],
            # object_position = [round(random.uniform(3.8, 4.4), 3),round(random.uniform(4.4, 5.0), 3),1.0],
            object_orientation = [math.pi,0,0 ],
            scale=1.0,
            obj_name='Book_B',
            fixed_base=False,
        )
        self.object_ids.append("elementP_id")  

        self.elementQ_id = self.pb_client.load_object(
            model_path = "./URDF_models/book_2/model.urdf",
            object_position = [4.2,0.8,1.0],
            # object_position = [round(random.uniform(3.8, 4.4), 3),round(random.uniform(0.5, 1), 3),1.0],
            object_orientation = [math.pi,0,0 ],
            scale=1.0,
            obj_name='Book_C',
            fixed_base=False,
        )
        self.object_ids.append("elementQ_id")

        self.elementR_id = self.pb_client.load_object(
            model_path = "./URDF_models/book_2/model.urdf",
            object_position = [4.2,0.7,1.0],
            #object_position = [round(random.uniform(3.8, 4.4), 3),round(random.uniform(0.5, 1), 3),1.0],
            object_orientation = [math.pi,0,0 ],
            scale=1.0,
            obj_name='Book_D',
            fixed_base=False,
        )
        self.object_ids.append("elementR_id")
        
        # ----------------------------------------------------------------
        # Set element colors
        # ----------------------------------------------------------------
        self.visualizer = PbVisualizer(pb_client)
        self.visualizer.set_elementA_visual_color(self.elementA_id[0])
        self.visualizer.set_elementB_visual_color(self.elementB_id[0])
        # self.visualizer.set_elementB_visual_color(self.elementB2_id)
        self.visualizer.set_elementC_visual_color(self.elementC_id[0])
        self.visualizer.set_elementD_visual_color(self.elementD_id[0])
        self.visualizer.set_elementE_visual_color(self.elementE_id[0])
        self.visualizer.set_elementE_visual_color(self.elementF_id[0])
        self.visualizer.set_elementE_visual_color(self.elementG_id[0])
        self.visualizer.set_elementE_visual_color(self.elementH_id[0])
        self.visualizer.set_elementE_visual_color(self.elementI_id[0])

    