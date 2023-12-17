# ji suan dao suo you zhang ai wu de zui jin ju li
import matplotlib.pyplot as plt
import numpy as np

def point_to_segment_distance(point, segment):
    """计算点到线段的最短距离，并返回最近点的坐标"""
    p1, p2 = np.array(segment[0]), np.array(segment[1])
    p = np.array(point)
    line_vec = p2 - p1
    p1_to_p = p - p1
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    p1_to_p_scaled = p1_to_p / line_len
    t = np.dot(line_unitvec, p1_to_p_scaled)
    if t < 0.0:
        return np.linalg.norm(p1_to_p), p1
    elif t > 1.0:
        return np.linalg.norm(p - p2), p2
    nearest = p1 + line_vec * t
    return np.linalg.norm(p - nearest), nearest

def point_to_rectangle_distance(point, rectangle):
    """计算点到矩形的最短距离，并返回最近点的坐标"""
    min_distance = float('inf')
    nearest_point = None
    for i in range(len(rectangle)):
        segment = [rectangle[i], rectangle[(i+1) % len(rectangle)]]
        distance, nearest = point_to_segment_distance(point, segment)
        if distance < min_distance:
            min_distance = distance
            nearest_point = nearest
    return min_distance, nearest_point

def plot_point_to_rectangles(point, rectangles):
    """绘制点到一组矩形的最短路径线段"""
    plt.figure(figsize=(8, 6))
    for rectangle in rectangles:
        # 绘制矩形
        x, y = zip(*rectangle, rectangle[0])  # Closes the rectangle
        plt.plot(x, y, 'b-')

        # 计算并绘制点到矩形的最短路径
        _, nearest_point = point_to_rectangle_distance(point, rectangle)
        plt.plot([point[0], nearest_point[0]], [point[1], nearest_point[1]], 'r--')

    # 绘制点
    plt.plot(point[0], point[1], 'ro')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Shortest Paths from Point to Rectangles')
    plt.grid(True)
    plt.show()

# 测试
rectangles = [
    [[3.1862777365475883, 5.069626060035825], [3.833652749660611, 5.069626060035825], [3.833652749660611, 5.10759665825665], [3.1862777365475883, 5.10759665825665]],
    [[3.8342374981641765, 5.682189099311828], [4.409681093573571, 5.682189099311828], [4.409681093573571, 5.74132460463047], [3.8342374981641765, 5.74132460463047]],
    [[3.8342374981641756, 5.095949591517448], [4.40968109357357, 5.095949591517448], [4.40968109357357, 5.158115598142147], [3.8342374981641756, 5.158115598142147]],
    [[4.393690905094146, 5.135198701739311], [4.40968109357357, 5.135198701739311], [4.40968109357357, 5.701363785147667], [4.393690905094146, 5.701363785147667]]
]
point = [6, 5.5]  # 示例点

plot_point_to_rectangles(point, rectangles)

