# The step2 aims to shinengchang
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# 求两个点之间的距离
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
# 求两个点之间线段对应的中点
def midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
# 这个函数的作用是把四边形抽象为直线，把门抽象为两条线段，输入矩形，返回线段
def find_farthest_midpoints(edges):
    """Find the two farthest midpoints of the edges of a quadrilateral."""
    # Calculate midpoints of all edges
    midpoints = [midpoint(edges[i], edges[(i + 1) % len(edges)]) for i in range(len(edges))]

    # Initialize maximum distance and point pair
    max_distance = 0
    farthest_pair = None

    # Compare each pair of midpoints to find the farthest pair
    for i in range(len(midpoints)):
        for j in range(i + 1, len(midpoints)):
            dist = distance(midpoints[i], midpoints[j])
            if dist > max_distance:
                max_distance = dist
                farthest_pair = (midpoints[i], midpoints[j])

    return farthest_pair
# 此函数的作用是计算两条线段的交点
def line_intersection(line1, line2):
    """Find the intersection of two lines (each defined by two points)."""
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('Lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
# 和line_intersection共同作用得到修正后的target坐标
def find_correct_target(after_point, before_point, zhou_point, target):
    """Find the midpoint of the line segment connecting o (intersection of l1 and l2) and before_point."""
    # Line l1: connecting zhou_point and before_point
    l1 = (zhou_point, before_point)

    # Line l2: connecting target and after_point
    l2 = (target, after_point)

    # Find intersection o of l1 and l2
    o = line_intersection(l1, l2)

    # Find midpoint (correct_target) of the line segment connecting o and before_point
    correct_target = midpoint(o, before_point)

    return correct_target
# 这个函数的作用是提取抽象为门的线段的转轴以及另外一个端点前后的坐标
def find_remaining_and_closest_points(farthest_midpoints_before, farthest_midpoints_after):
    """Find the remaining two points and the closest point from before set after removing the closest pair."""
    all_points = list(farthest_midpoints_before) + list(farthest_midpoints_after)

    # Initialize minimum distance and point pair
    min_distance = float('inf')
    closest_pair = None

    # Compare each pair of points to find the closest pair
    for i in range(len(all_points)):
        for j in range(i + 1, len(all_points)):
            dist = distance(all_points[i], all_points[j])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (all_points[i], all_points[j])

    # Remove the closest pair from all points
    remaining_points = [point for point in all_points if point not in closest_pair]

    # Identify which points belong to which set
    before_point = remaining_points[0] if remaining_points[0] in farthest_midpoints_before else remaining_points[1]
    after_point = remaining_points[0] if remaining_points[0] in farthest_midpoints_after else remaining_points[1]

    # Find the point from before set in the closest pair
    zhou_point = closest_pair[0] if closest_pair[0] in farthest_midpoints_before else closest_pair[1]

    return before_point, after_point, zhou_point
# 定义一个函数来提取在z pingmian

def get_edges_at_z(box, z_value):
    # 提取每个盒子的底部和顶部角点
    bottom_corners = box[:4]
    top_corners = box[4:]

    # 存储在z=0.85平面上的边
    edges_on_plane = []

    # 检查每一对底部和顶部角点
    for b, t in zip(bottom_corners, top_corners):
        # 如果一个角点在平面下方，另一个在上方，则边与平面相交
        if (b[2] <= z_value and t[2] >= z_value) or (b[2] >= z_value and t[2] <= z_value):
            # 使用线性插值找到交点
            ratio = (z_value - b[2]) / (t[2] - b[2])
            x = b[0] + ratio * (t[0] - b[0])
            y = b[1] + ratio * (t[1] - b[1])
            edges_on_plane.append([x, y])

    return edges_on_plane
all_boxes_range=[[[4.098999999999999, 5.419, 1.054], [4.101, 5.419, 1.054], [4.101, 5.421, 1.054], [4.098999999999999, 5.421, 1.054], [4.098999999999999, 5.419, 1.0559999999999998], [4.101, 5.419, 1.0559999999999998], [4.101, 5.421, 1.0559999999999998], [4.098999999999999, 5.421, 1.0559999999999998]], [[3.1862777365475883, 5.069626060035825, 0.32445440387725766], [3.833652749660611, 5.069626060035825, 0.32445440387725766], [3.833652749660611, 5.10759665825665, 0.32445440387725766], [3.1862777365475883, 5.10759665825665, 0.32445440387725766], [3.1862777365475883, 5.069626060035825, 1.9208873894214626], [3.833652749660611, 5.069626060035825, 1.9208873894214626], [3.833652749660611, 5.10759665825665, 1.9208873894214626], [3.1862777365475883, 5.10759665825665, 1.9208873894214626]], [[3.211781252744793, 4.954778346326948, 0.9621310020089143], [3.245482742789387, 4.954778346326948, 0.9621310020089143], [3.245482742789387, 4.991910760191083, 0.9621310020089143], [3.211781252744793, 4.991910760191083, 0.9621310020089143], [3.211781252744793, 4.954778346326948, 1.3775105144977564], [3.245482742789387, 4.954778346326948, 1.3775105144977564], [3.245482742789387, 4.991910760191083, 1.3775105144977564], [3.211781252744793, 4.991910760191083, 1.3775105144977564]], [[3.8342374981641765, 5.682189099311828, 0.015757085800170767], [4.409681093573571, 5.682189099311828, 0.015757085800170767], [4.409681093573571, 5.74132460463047, 0.015757085800170767], [3.8342374981641765, 5.74132460463047, 0.015757085800170767], [3.8342374981641765, 5.682189099311828, 2.049774296760559], [4.409681093573571, 5.682189099311828, 2.049774296760559], [4.409681093573571, 5.74132460463047, 2.049774296760559], [3.8342374981641765, 5.74132460463047, 2.049774296760559]], [[3.8342374981641756, 5.095949591517448, 0.015757085800170767], [4.40968109357357, 5.095949591517448, 0.015757085800170767], [4.40968109357357, 5.158115598142147, 0.015757085800170767], [3.8342374981641756, 5.158115598142147, 0.015757085800170767], [3.8342374981641756, 5.095949591517448, 2.049774296760559], [4.40968109357357, 5.095949591517448, 2.049774296760559], [4.40968109357357, 5.158115598142147, 2.049774296760559], [3.8342374981641756, 5.158115598142147, 2.049774296760559]], [[3.834237498164176, 5.135198701739311, 1.8739398140907284], [4.409681093573569, 5.135198701739311, 1.8739398140907284], [4.409681093573569, 5.701363785147667, 1.8739398140907284], [3.834237498164176, 5.701363785147667, 1.8739398140907284], [3.834237498164176, 5.135198701739311, 2.049774296760559], [4.409681093573569, 5.135198701739311, 2.049774296760559], [4.409681093573569, 5.701363785147667, 2.049774296760559], [3.834237498164176, 5.701363785147667, 2.049774296760559]], [[3.834237498164177, 5.135198701739311, 0.015757085800170517], [4.409681093573571, 5.135198701739311, 0.015757085800170517], [4.409681093573571, 5.701363785147667, 0.015757085800170517], [3.834237498164177, 5.701363785147667, 0.015757085800170517], [3.834237498164177, 5.135198701739311, 0.3738451318740845], [4.409681093573571, 5.135198701739311, 0.3738451318740845], [4.409681093573571, 5.701363785147667, 0.3738451318740845], [3.834237498164177, 5.701363785147667, 0.3738451318740845]], [[4.393690905094146, 5.135198701739311, 0.01575708580017121], [4.40968109357357, 5.135198701739311, 0.01575708580017121], [4.40968109357357, 5.701363785147667, 0.01575708580017121], [4.393690905094146, 5.701363785147667, 0.01575708580017121], [4.393690905094146, 5.135198701739311, 2.049774296760559], [4.40968109357357, 5.135198701739311, 2.049774296760559], [4.40968109357357, 5.701363785147667, 2.049774296760559], [4.393690905094146, 5.701363785147667, 2.049774296760559]], [[3.8731993994712823, 5.134198701739311, 0.7832930037975309], [4.400690905094146, 5.134198701739311, 0.7832930037975309], [4.400690905094146, 5.702363785147667, 0.7832930037975309], [3.8731993994712823, 5.702363785147667, 0.7832930037975309], [3.8731993994712823, 5.134198701739311, 0.8234811943173409], [4.400690905094146, 5.134198701739311, 0.8234811943173409], [4.400690905094146, 5.702363785147667, 0.8234811943173409], [3.8731993994712823, 5.702363785147667, 0.8234811943173409]], [[3.873199399471282, 5.134198701739312, 1.3586930910348891], [4.401190314531325, 5.134198701739312, 1.3586930910348891], [4.401190314531325, 5.702930300474167, 1.3586930910348891], [3.873199399471282, 5.702930300474167, 1.3586930910348891], [3.873199399471282, 5.134198701739312, 1.3986151036024093], [4.401190314531325, 5.134198701739312, 1.3986151036024093], [4.401190314531325, 5.702930300474167, 1.3986151036024093], [3.873199399471282, 5.702930300474167, 1.3986151036024093]]]
open_before=[[[3.803266899943351, 5.094949591517448, 0.324454403877258], [3.8412374981641775, 5.094949591517448, 0.324454403877258], [3.8412374981641775, 5.74232460463047, 0.324454403877258], [3.803266899943351, 5.74232460463047, 0.324454403877258], [3.803266899943351, 5.094949591517448, 1.9208873894214626], [3.8412374981641775, 5.094949591517448, 1.9208873894214626], [3.8412374981641775, 5.74232460463047, 1.9208873894214626], [3.803266899943351, 5.74232460463047, 1.9208873894214626]]]
open_after=[[[3.1862777365475883, 5.069626060035825, 0.32445440387725766], [3.833652749660611, 5.069626060035825, 0.32445440387725766], [3.833652749660611, 5.10759665825665, 0.32445440387725766], [3.1862777365475883, 5.10759665825665, 0.32445440387725766], [3.1862777365475883, 5.069626060035825, 1.9208873894214626], [3.833652749660611, 5.069626060035825, 1.9208873894214626], [3.833652749660611, 5.10759665825665, 1.9208873894214626], [3.1862777365475883, 5.10759665825665, 1.9208873894214626]]]

fig, ax = plt.subplots()
before_edges_on_plane = []
after_edges_on_plane = []
# 处理每个盒子并在z=0.85平面绘制边
for box in open_before:
    edges = get_edges_at_z(box, 0.85)
    if edges:
        # 假设每个盒子在平面上有两条边
        polygon = Polygon(edges, closed=False, edgecolor='r', fill=None)
        ax.add_patch(polygon)
        before_edges_on_plane.append(edges)
#print(all_edges_on_plane)
for box in open_after:
    edges = get_edges_at_z(box, 0.85)
    if edges:
        # 假设每个盒子在平面上有两条边
        polygon = Polygon(edges, closed=False, edgecolor='r', fill=None)
        ax.add_patch(polygon)
        after_edges_on_plane.append(edges)
# print("before_edges_on_plane=",before_edges_on_plane,"after_edges_on_plane=",after_edges_on_plane)
#  Flatten the nested lists
before_edges_flat = before_edges_on_plane[0]
after_edges_flat = after_edges_on_plane[0]
# Find the closest midpoints for both quadrilaterals
farthest_midpoints_before = find_farthest_midpoints(before_edges_flat)
farthest_midpoints_after = find_farthest_midpoints(after_edges_flat)
print("farthest_midpoints_before :",farthest_midpoints_before,"farthest_midpoints_after",farthest_midpoints_after)
# Find the remaining points
before_point, after_point, zhou_point = find_remaining_and_closest_points(farthest_midpoints_before, farthest_midpoints_after)

print("before_point:",before_point,"after_point:",after_point,"zhou_point: ",zhou_point)

# 在z=0.85平面上添加散点图点（4.2, 5.5）
target=(4.2,5.5)
correct_target = find_correct_target(after_point, before_point, zhou_point, target)
print("correct_point:",correct_target)
ax.scatter(4.2, 5.5, color='green')

# 设置图的限制
ax.set_xlim(1, 6)
ax.set_ylim(4, 8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Z=0.85 touying')
#
# 展示图表
plt.show()