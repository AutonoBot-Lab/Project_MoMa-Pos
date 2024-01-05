# Max Range: [-1.05667 1.06119305] 考虑建立最大半径为1.30303655的球体结构,输入:机械臂的DH矩阵的初始化参数以及每一个关节的角度范围
# 根据这段代码生成的图进行第一部的范围缩小，以目标物为中心，俯视图的可用standing position->l1=l0*cosa cosa=sqrt.(l0^2-(h1-h0)^2)/l0,base的高度=0.8+0.15=0.95
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
def specific_arm_range(h0,l0=1.06119305,target_position=[0,0,0]):
    a=target_position[2]
    c=l0
    b=h0
    specific_range=math.sqrt(c**2-(b-a)**2)
    return specific_range


fig, ax = plt.subplots(figsize=(10, 10))

# Draw the base as a line
fig, ax = plt.subplots(figsize=(10, 10))

# Draw the base as a line
base_x = [-0.01, 0.01]
base_y = [0.6, 0.6]
ax.plot(base_x, base_y, color="blue", linewidth=5, label="Base")

# Draw a simplified arm as a line
arm = [(0, 0.6), (0, 0.6 + 1.3)]
ax.plot([point[0] for point in arm], [point[1] for point in arm], color="black", linewidth=5, label="Arm")

# Draw the arm's range as a dashed circle
arm_range_circle = patches.Circle((0, 0.6), 1.3, fill=False, linestyle='--', color="red", label="Arm Range")
ax.add_patch(arm_range_circle)

# Draw wheels and connection
wheel_radius = 0.1
left_wheel = patches.Circle((-0.3, wheel_radius), wheel_radius, facecolor="gray", label="Wheel")
right_wheel = patches.Circle((0.3, wheel_radius), wheel_radius, facecolor="gray")
ax.add_patch(left_wheel)
ax.add_patch(right_wheel)

# Connect wheels with a line
ax.plot([-0.3, 0.3], [wheel_radius, wheel_radius], color="gray", linewidth=2)

# Connect midpoint of wheel connection to the base
ax.plot([0, 0], [0.6, 2*wheel_radius], color="gray", linewidth=2)

# Draw the target point and line
target_point = patches.Circle((1.275, 0.3), 0.05, facecolor="red", label="Target")
ax.add_patch(target_point)
ax.plot([1.275, 1.275], [0, 0.3], color="red", linestyle='--')

# Setting the aspect ratio, limits, legend, and title
ax.set_aspect('equal', 'box')
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(0, 3)
ax.legend(loc="upper left")
ax.set_title("Arm with Base, Wheels, Range and Target")

plt.show()
