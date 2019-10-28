import bike
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import visualization as vi
from math import ceil

# 读取城市坐标

x = [2, 1.25, 2.75, 1.6, 2.4]
y = [3, 2.25, 2.25, 1.25, 1.25]
v = np.array([x, y])
n = v.shape[1]

# 各区域之间的距离
D = np.array([[0, 6, 12, 10, 5],
              [6, 0, 8, 7, 6],
              [12, 8, 0, 4, 7],
              [10, 7, 4, 0, 5],
              [5, 6, 7, 5, 0]])

# 定义参数
C_max = bike.C_max
td = bike.td

m = 50  # 蚂蚁数量
dim = 15
alpha = 1  # 信息素重要程度因子
beta = 2  # 启发函数重要程度因子
rho = 0.1  # 信息素挥发因子
Q = 0.0001  # 常系数
# Eta = 1.0 / D  # 启发函数
Tau = np.ones((n, n))  # 信息素矩阵
Table = np.zeros((m, dim), dtype=int)  # 路径记录表
iter = 0  # 迭代次数初值
iter_max = 300  # 最大迭代次数
Route_best = np.zeros((iter_max, dim), dtype=int)  # 各代最佳路径
Length_best = np.zeros((iter_max, 1))  # 各代最佳路径的长度
Length_ave = np.zeros((iter_max, 1))  # 各代路径的平均长度
q_ave = np.zeros((iter_max, 1)).tolist()
q_max = np.zeros((iter_max, 1)).tolist()
# 迭代寻找最佳路径
while iter < iter_max:
    # 随机产生各个蚂蚁的起点城市
    Table[:, 0] = np.random.randint(1, n, m)
    T = 60
    t = 0
    # 构建解空间
    area_index = set(np.arange(n))
    q_total = np.zeros((m, 1)).tolist()
    # 逐个蚂蚁路径选择
    for i in range(m):
        buf = [-1, 0, 10, 15, 10, 10]  # 各个小区有几辆车
        C_max = 20
        C = 0
        q = 0
        t = 0
        # 逐个城市路径选择
        for j in range(1, dim):
            tabu = Table[i, j - 1]  # 当前所处的节点
            if t + D[0][tabu] > T:
                break
            if j == 1:
                t += D[0, tabu]
                need = vi.get_requirement(buf, t)[tabu + 1]
                if need < 0:  # 小区缺车的情况
                    b = max(-C, need)
                else:  # 小区多车的情况
                    b = min(C_max - C, need, ceil(buf[tabu + 1]))
                q += abs(b)
                buf[tabu + 1] -= b
                C += b
                t += td * abs(b)
            allow = np.array(list(area_index - set([tabu]) - set([0])))  # 待访问区域集合
            P = allow.astype(float)
            temp_C = np.zeros((1, n))
            temp_B = np.zeros((1, n))
            temp_t = np.zeros((1, n))
            temp_q = np.zeros((1, n))
            # 计算城市间转移概率
            for k in range(len(allow)):
                temp_t[0][k] += D[tabu, allow[k]]

                need = vi.get_requirement(buf, temp_t[0][k] + t)[allow[k] + 1]
                if need < 0:  # 小区缺车的情况
                    b = max(-C, need)
                else:  # 小区多车的情况
                    b = min(C_max - C, need, ceil(buf[allow[k] + 1]))
                temp_B[0][k] = b
                temp_C[0][k] += b
                temp_q[0][k] += abs(b)
                temp_t[0][k] += abs(b) * td
                if b == 0:
                    tb = 0.1
                else:
                    tb = b
                P[k] = (Tau[tabu, allow[k]]) ** alpha * (abs(tb) / D[tabu, allow[k]]) ** beta
            P = P / sum(P)
            # 轮盘赌法选择下一个访问城市
            PC = np.cumsum(P)
            target_index = np.where(PC > np.random.random())
            temp_target_index = np.array(target_index[-1])[0]
            target = allow[temp_target_index]
            Table[i, j] = target
            temp_target_index = [np.array(target_index[-1])[0]]
            C += int(temp_C[0][temp_target_index])
            t1 = t
            t += int(temp_t[0][temp_target_index])
            t2 = t
            q += int(temp_q[0][temp_target_index])
            buf = vi.change_buf(buf, t1, t2)

        q_total[i] = q
    q_ave[iter] = np.average(q_total)
    q_max[iter] = np.max(q_total)

    print(Table)
    # 计算各个蚂蚁的路径距离
    # Length = np.zeros((m, 1))
    # for i in range(m):
    #     Route = Table[i, :]
    #     for j in range(n - 1):
    #         Length[i] += D[Route[j], Route[j + 1]]
    #
    #     Length[i] += D[Route[-1], Route[0]]

    # # 计算最短路径距离及平均距离
    # max_q = np.max([q_total])
    # max_index = np.argmin(q_total)
    # if iter == 0:
    #     Length_best[iter] = max_q
    #     Length_ave[iter] = np.mean(Length)
    #     Route_best[iter] = Table[max_index]
    # else:
    #     Length_best[iter] = min(Length_best[iter - 1], max_q)
    #     Length_ave[iter] = np.mean(Length)
    #     if Length_best[iter] == max_q:
    #         Route_best[iter] = Table[max_index]
    #     else:
    #         Route_best[iter] = Route_best[iter - 1]

    # 更新信息素
    Delta_Tau = np.zeros((n, n))
    # 逐个蚂蚁计算
    for i in range(m):
        # 逐个区域计算
        for j in range(n):
            Delta_Tau[Table[i, j], Table[i, j + 1]] += q * Q

        Delta_Tau[Table[i, -1], Table[i, 0]] += q * Q

    Tau = (1 - rho) * Tau + Delta_Tau
    # 迭代次数加1，清空路径记录表
    iter = iter + 1
    Table = np.zeros((m, dim), dtype=int)

# 结果显示
x = np.arange(iter_max) + 1
plt.plot(x, q_ave, color='red')
plt.plot(x, q_max, color='blue')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title('平均调度量和最大调度量')
plt.savefig('./save/' + str('Result') + '.png')
plt.show()

# Shortest_Length = np.min(Length_best)
# index = np.argmin(Length_best)
# Shortest_Route = Route_best[index, :]
# print('最短距离:', Shortest_Length)
# print('最短路径:', Shortest_Route)

# # ## 绘图
# plt.figure(1)
# plt.plot((v[Shortest_Route, 0]), (v[Shortest_Route, 1]), color="red", linestyle="-")
# plt.plot(((v[Shortest_Route[0], 0]), (v[Shortest_Route[-1], 0])),
#          ((v[Shortest_Route[0], 1]), (v[Shortest_Route[-1], 1])), color="red", linestyle="-")
# plt.grid(True)
# plt.figure(2)
# plt.plot(np.arange(iter_max), Length_best, 'b', label='Shortest Distance')
# plt.plot(np.arange(iter_max), Length_ave, 'r', label='Average Distance')
# plt.legend()
# plt.xlabel('Iteration times')
# plt.ylabel('Distance')
# plt.show()
