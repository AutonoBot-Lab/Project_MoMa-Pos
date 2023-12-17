# Correct the UR5e's DH parameters based on the provided values
import numpy as np
d_corrected = [0.1634, 0, 0, 0.14, 0.13, 0.1]
a_corrected = [0, -0.425, -0.5, 0, 0, 0]
alpha_corrected = [np.pi/2, 0, 0, np.pi/2, -np.pi/2, 0]

# Modify the end_effector_position function to incorporate the corrected UR5e's DH parameters
def end_effector_position_corrected(theta):
    T = np.eye(4)
    for i in range(6):
        # Calculate transformation matrix using corrected DH parameters for UR5e
        Ti = np.array([
            [np.cos(theta[i]), -np.sin(theta[i])*np.cos(alpha_corrected[i]), np.sin(theta[i])*np.sin(alpha_corrected[i]), a_corrected[i]*np.cos(theta[i])],
            [np.sin(theta[i]), np.cos(theta[i])*np.cos(alpha_corrected[i]), -np.cos(theta[i])*np.sin(alpha_corrected[i]), a_corrected[i]*np.sin(theta[i])],
            [0, np.sin(alpha_corrected[i]), np.cos(alpha_corrected[i]), d_corrected[i]],
            [0, 0, 0, 1]
        ])
        T = np.dot(T, Ti)
    return T[:3, 3]

# Calculate the end effector positions for various joint configurations
positions_corrected = []

# Joint angle samples: uniformly sample 10 points around the circle for each joint
angles = np.linspace(-np.pi, np.pi, 10)

# Use a six-level nested loop to iterate over all combinations
for theta1 in angles:
    for theta2 in angles:
        for theta3 in angles:
            for theta4 in angles:
                for theta5 in angles:
                    for theta6 in angles:
                        pos = end_effector_position_corrected([theta1, theta2, theta3, theta4, theta5, theta6])
                        positions_corrected.append(pos)

# Convert the list of positions to a numpy array for easier calculations
positions_corrected = np.array(positions_corrected)

# Calculate the minimum and maximum x, y, z coordinates of the end effector
min_pos_corrected = positions_corrected.min(axis=0)
max_pos_corrected = positions_corrected.max(axis=0)

print(min_pos_corrected, max_pos_corrected)
#[-1.05667    -1.02377577 -0.90338962] [1.06119305 1.07221541 1.23723517]