import random
from mcts_helps import MCTSHelps, Node
MAX_DEPTH = 5
GAMMA = 0.9  # 常见的折扣因子
ACTIONS = ["right", "left", "forward", "back"]

# def simulate(s, T, depth, potential_map, goal_state):
#     if depth > MAX_DEPTH or s == goal_state:
#         return 0
#     if s not in T:
#         T[s] = Node(s)
#     if not T[s].children:
#         expand_node(T[s], T, potential_map, goal_state)
#     if T[s].visit_count == 0:
#         rollout_reward = rollout(s, depth, potential_map, goal_state)
#         T[s].total_reward += rollout_reward  # 累加奖励
#         T[s].visit_count += 1  # 增加访问次数
#
#     action = MCTSHelps.select_action(s, T, potential_map)
#     if action is None:  # 检查是否有可用动作
#         return 0  # 或者其他合适的处理
#     new_state = MCTSHelps.apply_action(s, action, potential_map)
#     reward = MCTSHelps.reward(s, action, new_state, goal_state, potential_map)
#
#     R = reward + GAMMA * simulate(new_state, T, depth + 1, potential_map, goal_state)
#     MCTSHelps.update_tree(T, s, action, R)
#     return R

def simulate(s, T, depth, potential_map, goal_state):
    if depth > MAX_DEPTH or s == goal_state:
        return 0
    if s not in T:
        T[s] = Node(s)
    if not T[s].children:
        expand_node(T[s], T, potential_map, goal_state)
    # 动作选择
    action = MCTSHelps.select_action(s, T, potential_map)
    if action is None:  # 检查是否有可用动作
        return 0

    new_state = MCTSHelps.apply_action(s, action, potential_map)
    # 在这里执行rollout
    if T[new_state].visit_count == 0:
        rollout_reward = rollout(new_state, 5, potential_map, goal_state)
        T[new_state].total_reward += rollout_reward
        T[new_state].visit_count += 1
    reward = MCTSHelps.reward(s, action, new_state, goal_state, potential_map)
    R = reward + GAMMA * simulate(new_state, T, depth + 1, potential_map, goal_state)
    MCTSHelps.update_tree(T, s, action, R)
    return R
def expand_node(node, T, potential_map,goal_state):

    for action in ACTIONS:
        new_state = MCTSHelps.apply_action(node.state, action, potential_map)
        if new_state not in T:  # 确保不重复创建节点
            new_node = Node(new_state, parent=node)
            T[new_state] = new_node
            node.children[action] = new_node


def rollout(s, depth, potential_map, goal_state):
    """
    对未探索路径进行快速模拟。

    :param s: 当前状态。
    :param depth: 当前深度。
    :param potential_map: 势能图。
    :param goal_state: 目标状态。
    :return: 在此路径上累积的奖励。
    """
    print("s :", s, "Depth :", depth)
    if depth > MAX_DEPTH or s == goal_state:
        return 0  # 达到最大深度或目标状态时停止
    action = random.choice(ACTIONS)
    new_state = MCTSHelps.apply_action(s, action, potential_map)
    reward = MCTSHelps.reward(s, action, new_state, goal_state, potential_map)
    return reward + GAMMA * rollout(new_state, depth + 1, potential_map, goal_state)
def search(N, potential_map, start_state, goal_state):
    T = {}  # 决策树，存储节点

    for _ in range(N):
        s = start_state  # 从根节点开始
        simulate(s, T, 0, potential_map, goal_state)

    # 选择访问次数最多的动作作为最佳动
    best_action = None
    best_visit = -1
    for action, child in T[start_state].children.items():
        print(f"Action: {action}, Total Reward: {child.total_reward}, Visit Count: {child.visit_count}")
        if child.visit_count > best_visit:
            best_visit = child.visit_count
            best_action = action

    return best_action
