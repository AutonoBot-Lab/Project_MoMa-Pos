import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
class Parser:
    def __init__(self, obstacle):
        self.obstacle = obstacle
    def draw_3d(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for box in self.obstacle:
            edges = [
                [box[0], box[1], box[5], box[4]],
                [box[7], box[6], box[2], box[3]],
                [box[0], box[3], box[2], box[1]],
                [box[7], box[4], box[5], box[6]],
                [box[0], box[4], box[7], box[3]],
                [box[1], box[5], box[6], box[2]],
            ]
            ax.add_collection3d(Poly3DCollection(edges, alpha=.25, linewidths=1, edgecolors='r'))
        # ax.set_xlim([-1.02, 10])
        # ax.set_ylim([-1.02, 10])
        ax.set_xlim([3, 6])
        ax.set_ylim([4, 6])
        ax.set_zlim([-0.02, 2])
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        ax.view_init(elev=20, azim=170)
        plt.show()

    def draw_xy(self):
        # fig, ax = plt.subplots()
        rectangles = []  # 用于存储所有矩形的顶点

        for box in self.obstacle:
            # 找到每个长方体在XY平面上的最小和最大X、Y坐标
            min_x = min([point[0] for point in box])
            max_x = max([point[0] for point in box])
            min_y = min([point[1] for point in box])
            max_y = max([point[1] for point in box])

            # 创建矩形的四个角点
            rectangle_points = [
                [min_x, min_y],
                [max_x, min_y],
                [max_x, max_y],
                [min_x, max_y]
            ]
            rectangles.append(rectangle_points)

            # 绘制矩形（XY平面上的投影）
        #     rectangle = plt.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, fill=False, edgecolor='red',
        #                               linewidth=1)
        #     ax.add_patch(rectangle)
        #
        # # 设置坐标轴标签和范围
        # ax.set_xlabel('X Axis')
        # ax.set_ylabel('Y Axis')
        # ax.set_xlim([-2, 10])  # 根据需要调整范围
        # ax.set_ylim([-2, 10])  # 根据需要调整范围
        #
        # plt.show()

        return rectangles