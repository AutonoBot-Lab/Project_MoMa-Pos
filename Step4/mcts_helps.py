import math
import random
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visit_count = 0
        self.total_reward = 0

    def __repr__(self):
        return f"Node(state={self.state}, visit_count={self.visit_count}, total_reward={self.total_reward}) "

class MCTSHelps:
    @staticmethod
    def initialize_tree(start_state):
        """
        创建初始节点。

        :param start_state: 初始状态
        :return: 创建的树的根节点
        """
        root = Node(start_state)
        print("initialize_tree Successfully!", root)
        return root

    @staticmethod
    def sample_from_belief(belief_state, potential_map):
        return random.choice(list(potential_map.keys()))



    @staticmethod
    def select_action(s, T, potential_map,exploration_weight=1.414):
        """
        根据当前状态和决策树选择动作。

        :param s: 当前状态。
        :param T: 决策树。
        :param potential_map: 势能图。
        :param exploration_weight: 探索权重，用于平衡探索和利用。
        :return: 选择的动作。
        """
        if s not in T or not T[s].children:
            return None  # 如果没有子节点，则无法选择动作

        best_action = None
        best_score = float('-inf')

        for action, child_node in T[s].children.items():
            # 如果有未访问过的子节点，则立即选择该动作
            if child_node.visit_count == 0:
                return action

            # 计算 UCB 分数
            exploitation = child_node.total_reward / child_node.visit_count
            exploration = math.sqrt(math.log(T[s].visit_count) / child_node.visit_count)
            ucb_score = exploitation + exploration_weight * exploration

            if ucb_score > best_score:
                best_score = ucb_score
                best_action = action

        return best_action

    @staticmethod

    def is_valid_position(state, potential_map, tolerance=0.01):
        x, y = state
        # 检查势能图中是否有与给定状态足够接近的点
        for (px, py) in potential_map.keys():
            if abs(px - x) <= tolerance and abs(py - y) <= tolerance:
                return True
        return False

    @staticmethod
    def apply_action(current_state, action, potential_map):
        """
        应用动作并返回新状态。

        :param current_state: 当前状态，例如 (x, y) 坐标。
        :param action: 选择的动作，例如 "向东移动"。
        :param potential_map: 势能图。
        :return: 新状态。
        """
        x, y = current_state
        move_distance = 0.05  # 每次移动的距离

        if action == "right":
            new_state = (x + move_distance, y)
        elif action == "left":
            new_state = (x - move_distance, y)
        elif action == "forward":
            new_state = (x, y + move_distance)
        elif action == "back":
            new_state = (x, y - move_distance)
        else:
            raise ValueError("未知动作")

        # 检查新状态是否有效（在势能图范围内）
        if MCTSHelps.is_valid_position(new_state, potential_map):
            return new_state
        else:
            print(new_state, "not in this map!")
            return current_state

    @staticmethod
    def find_closest_potential_value(state, potential_map, tolerance =0.01):
        closest_value = None
        min_distance = float('inf')
        for (px, py), potential in potential_map.items():
            distance = math.sqrt((state[0] - px) ** 2 + (state[1] - py) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_value = potential
        return closest_value if closest_value is not None else 0
    @staticmethod
    def reward(s, action, new_state, goal_state, potential_map):
        """
        根据执行动作后的状态变化计算奖励值。
        :param s: 当前状态。
        :param action: 执行的动作。
        :param new_state: 新状态。
        :param goal_state: 目标状态。
        :param potential_map: 势能图。
        :return: 计算得到的奖励值。
        """
        # 计算到目标状态的距离
        distance_to_goal = math.sqrt((new_state[0] - goal_state[0]) ** 2 + (new_state[1] - goal_state[1]) ** 2)
        # 获取新状态的势能值
        s_potential = MCTSHelps.find_closest_potential_value(s, potential_map, 0.01)
        new_state_potential = MCTSHelps.find_closest_potential_value(new_state, potential_map, 0.01)
        potential_value = new_state_potential - s_potential

        # 距离目标的奖励（距离越小，奖励越大）
        distance_reward = 1 / (distance_to_goal + 1e-6)  # 添加小量以避免除以0

        # 势能的奖励（势能越低，奖励越大）
        potential_reward = -potential_value * 1000  # 假设势能是负值越小越好

        # 综合奖励
        total_reward = distance_reward + potential_reward

        return total_reward

    @staticmethod
    def update_tree(T, s, action, R):
        """
        更新决策树的节点信息。

        :param T: 决策树。
        :param s: 当前状态。
        :param action: 执行的动作。
        :param R: 从该动作获得的奖励。
        """
        node = T[s]
        node.visit_count += 1
        node.total_reward += R

        # 向上传播奖励和访问次数
        while node.parent is not None:
            node = node.parent
            node.visit_count += 1
            node.total_reward += R