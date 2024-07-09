import queue as Q
import time
class TSP:
    def __init__(self, input_matrix, input_potential_map):
        self.input_matrix = input_matrix
        self.potential_map = input_potential_map
        self.node_init = 1


    def cost(self, node):
        sum = 0
        input_matrix = self.input_matrix

        remain = list(set(range(len(input_matrix))) - set(node))
        for i in range(1, len(node)):
            sum += input_matrix[node[i - 1]][node[i]]
        m1 = 0
        if remain:
            m1 = float('inf')
            for i in remain:
                if input_matrix[node[-1]][i] < m1:
                    m1 = input_matrix[node[-1]][i]
        sum += m1

        if sum == 0:  # if still in first node
            remain += [node[0]]
        for i in remain:
            m1, m2 = float('inf'), float('inf')
            for j in range(len(input_matrix)):
                if input_matrix[i][j] <= m1:
                    m1, m2 = input_matrix[i][j], m1
                elif input_matrix[i][j] < m2:
                    m2 = input_matrix[i][j]
            sum += (m1 + m2) / 2

        return float(sum)

    def node_child(self, node_state):
        return list(set(range(len(self.input_matrix))) - set(node_state))

    def solve(self, q, state_num):
        cost_res = 0  # 用于存储到目前为止找到的最低成本路径的成本
        node_state_res = []  # 用于存储最低成本路径的节点序列
        B = float('inf')
        while (not q.empty()):
            cur_state = q.get()
            curr_cost = cur_state[0]
            node_state = cur_state[1]
            node_target = self.node_child(node_state)

            if not node_target:  # 这一小段代码的作用是当搜索过程中有了叶节点的时候怎么办，剪枝的操作在这一部分实现
                if curr_cost < B:
                    node_state_res = node_state
                    cost_res = curr_cost
                B = curr_cost
                store = []
                while not q.empty():
                    temp = q.get()
                    if abs(temp[0] - B) <= 0.1:
                        store.append(temp)
                for elem in store:
                    q.put(elem)

            state_num += len(node_target)
            for i in node_target:
                node_next = node_state + [i]
                cost_next = self.cost(node_next)
                if cost_next <= B:
                    q.put((cost_next, node_next))

        node_state_res = [elem + 1 for elem in node_state_res]
        return cost_res, node_state_res, state_num
    def Tsp_route(self):
        # 由于节点的编号是从1-N的，但是在矩阵中编号从0开始，因此都-1
        self.node_init -= 1
        q = Q.PriorityQueue()
        low_bound = self.cost([self.node_init])
        state_num = 1
        q.put((low_bound, [self.node_init]))
        start_time = time.time()
        # Solve TSP :)
        result = self.solve(q, state_num)
        points_route = [list(self.potential_map[b - 1].keys())[0] for b in result[1][1:]]
        # print("route cost:  %.2f" % result[0])
        # print("Generated Nodes : %d" % result[2])
        elapsed_time_step3 = (time.time() - start_time)
        # print("Open TSP route is:", result[1])

        return result[1], points_route, elapsed_time_step3