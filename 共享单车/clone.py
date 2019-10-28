import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# 读取城市坐标
v = np.array(pd.read_excel('city.xls'))
n = v.shape[0]

# 计算各城市之间的距离
D = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            D[i, j] = np.sqrt(sum((v[i] - v[j]) ** 2))
        else:
            D[i, j] = 1e-4

# 定义参数
m = 50  # 蚂蚁数量
alpha = 1  # 信息素重要程度因子
beta = 5  # 启发函数重要程度因子
rho = 0.1  # 信息素挥发因子
Q = 1  # 常系数
Eta = 1.0 / D  # 启发函数
Tau = np.ones((n, n))  # 信息素矩阵
Table = np.zeros((m, n), dtype=int)  # 路径记录表
iter = 0  # 迭代次数初值
iter_max = 200  # 最大迭代次数
Route_best = np.zeros((iter_max, n), dtype=int)  # 各代最佳路径
Length_best = np.zeros((iter_max, 1))  # 各代最佳路径的长度
Length_ave = np.zeros((iter_max, 1))  # 各代路径的平均长度

# 迭代寻找最佳路径
while iter < iter_max:
    # 随机产生各个蚂蚁的起点城市
    Table[:, 0] = np.random.randint(0, n, m)
    # 构建解空间
    citys_index = set([i for i in range(n)])
    # 逐个蚂蚁路径选择
    for i in range(m):
        # 逐个城市路径选择
        for j in range(1, n):
            tabu = Table[i, :j]  # 已访问的城市集合(禁忌表)
            allow = np.array(list(citys_index - set(tabu)))  # 待访问的城市集合
            P = allow.astype(float)
            # 计算城市间转移概率
            for k in range(len(allow)):
                P[k] = Tau[tabu[-1], allow[k]] ** alpha * Eta[tabu[-1], allow[k]] ** beta
            P = P / sum(P)
            # 轮盘赌法选择下一个访问城市
            PC = np.cumsum(P)
            target_index = np.where(PC > np.random.random())
            target = allow[np.array(target_index[0])[0]]
            Table[i, j] = target

    # 计算各个蚂蚁的路径距离
    Length = np.zeros((m, 1))
    for i in range(m):
        Route = Table[i, :]
        for j in range(n - 1):
            Length[i] += D[Route[j], Route[j + 1]]

        Length[i] += D[Route[-1], Route[0]]

    # 计算最短路径距离及平均距离
    min_Length = min(Length)
    min_index = np.argmin(Length)
    if iter == 0:
        Length_best[iter] = min_Length
        Length_ave[iter] = np.mean(Length)
        Route_best[iter] = Table[min_index]
    else:
        Length_best[iter] = min(Length_best[iter - 1], min_Length)
        Length_ave[iter] = np.mean(Length)
        if Length_best[iter] == min_Length:
            Route_best[iter] = Table[min_index]
        else:
            Route_best[iter] = Route_best[iter - 1]

    # 更新信息素
    Delta_Tau = np.zeros((n, n))
    # 逐个蚂蚁计算
    for i in range(m):
        # 逐个城市计算
        for j in range(n - 1):
            Delta_Tau[Table[i, j], Table[i, j + 1]] += Q / Length[i]

        Delta_Tau[Table[i, -1], Table[i, 0]] += Q / Length[i]

    Tau = (1 - rho) * Tau + Delta_Tau
    # 迭代次数加1，清空路径记录表
    iter = iter + 1
    Table = np.zeros((m, n), dtype=int)

# 结果显示
Shortest_Length = np.min(Length_best)
index = np.argmin(Length_best)
Shortest_Route = Route_best[index, :]
print('最短距离:', Shortest_Length)
print('最短路径:', Shortest_Route)

# ## 绘图
plt.figure(1)
plt.plot((v[Shortest_Route, 0]), (v[Shortest_Route, 1]), color="red", linestyle="-")
plt.plot(((v[Shortest_Route[0], 0]), (v[Shortest_Route[-1], 0])),
         ((v[Shortest_Route[0], 1]), (v[Shortest_Route[-1], 1])), color="red", linestyle="-")
plt.grid(True)
plt.figure(2)
plt.plot(np.arange(iter_max), Length_best, 'b', label='Shortest Distance')
plt.plot(np.arange(iter_max), Length_ave, 'r', label='Average Distance')
plt.legend()
plt.xlabel('Iteration times')
plt.ylabel('Distance')
plt.show()
