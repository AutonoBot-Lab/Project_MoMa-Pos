# 这段代码的作用是识别URDF模型的分类分为fixed revolute 以及prismatic
import xml.etree.ElementTree as ET

def classify_urdf_joints(urdf_content):
    # 解析XML内容
    root = ET.fromstring(urdf_content)

    # 初始化关节类型计数器
    joint_types = {"fixed": 0, "revolute": 0, "prismatic": 0}

    # 遍历所有关节并计数
    for joint in root.findall('.//joint'):  # 使用 './/joint' 来确保可以找到所有级别的joint标签
        joint_type = joint.get('type')  # 获取type属性
        if joint_type:
            joint_types[joint_type] += 1

    # 分类逻辑
    if joint_types["revolute"] > 0:
        return "revolute"
    elif joint_types["prismatic"] > 0:
        return "prismatic"
    elif joint_types["fixed"] == sum(joint_types.values()):  # 检查所有关节是否都是fixed
        return "fixed"
    else:
        return "unknown"

def count_urdf_joints(urdf_content):
    # 解析XML内容
    root = ET.fromstring(urdf_content)

    # 初始化关节类型计数器
    joint_types = {"fixed": 0, "revolute": 0, "prismatic": 0}

    # 遍历所有关节并计数
    for joint in root.findall('.//joint'):  # 使用 './/joint' 来确保可以找到所有级别的joint标签
        joint_type = joint.get('type')  # 获取type属性
        if joint_type in joint_types:
            joint_types[joint_type] += 1

    return joint_types
# 使用函数

def print_revolute_prismatic_joints(urdf_content):
    # 解析XML内容
    root = ET.fromstring(urdf_content)

    # 遍历所有关节并打印revolute和prismatic关节的信息
    for joint in root.findall('.//joint'):
        joint_type = joint.get('type')
        if joint_type in ["revolute", "prismatic"]:
            child_link = joint.find('child').get('link')
            parent_link = joint.find('parent').get('link')
            print(f"Joint name: {joint.get('name')}, Type: {joint_type}, Child link: {child_link}, Parent link: {parent_link}")
# /home/shaobeichen/robot/BestMan-step3/BestMan_Pybullet-master/Kitchen_models//models/Dishwasher/2085/mobility.urdf
urdf_file_path = '/home/shaobeichen/robot/BestMan-step3/BestMan_Pybullet-master/Kitchen_models//models/Fridge/10144/mobility.urdf'
with open(urdf_file_path, 'r') as file:
    urdf_content = file.read()

# 使用函数
classification = classify_urdf_joints(urdf_content)
joint_counts = count_urdf_joints(urdf_content)
sp_links=print_revolute_prismatic_joints(urdf_content)
print(f"Joint counts in the URDF model: {joint_counts}")
print(f"The URDF model is classified as: {classification}")

