import bike
from math import ceil
import numpy as np
import visualization as xu
import matplotlib.pyplot as plt

C_max = bike.C_max  # 车的容量
d = bike.d  # d(i, j)表示i到j的距离
B = bike.B  # B(i, t)表示i点在t时刻的需求量
T = bike.T  # 时间限制
td = bike.td  # 装卸一辆车的时间

# 定义部分参数
n = 6  # 小区数量(实际使用中把下标0弃用)
alpha = 2  # 信息素重要程度因子
beta = 1  # 启发函数重要程度因子
rho = 0.1  # 信息素挥发因子
Q = 0.1  # 常系数
Tau = np.ones((n, n))  # 信息素矩阵


class Ant(object):

    def __init__(self):
        self.path = [1]
        self.q = 0
        self.C = 0
        self.t = 0
        self.t_list = [0]  # 记下抵达每个小区的时间
        self.buf = [-10086, 0, 10, 15, 10, 10]
        while self.t < T:
            self.walk()

    def walk(self):  # 蚂蚁从i走到下一个小区j
        allow = set([2, 3, 4, 5])
        i = self.path[-1]
        allow.discard(i)  # 不能停在原地
        forbid = []
        for j in allow:  # 不能走向超时的点
            if self.t + d(i, j) > T:
                forbid.append(j)
        allow -= set(forbid)

        if len(allow) == 0:  # 无路可走的话，杀掉这只蚂蚁
            self.t = 10086  # 令时间无穷大(然后就超时了)
            return

        # 准备计算走到各点的概率
        P = []
        allow = list(allow)
        for j in allow:  # 假设走某一点j
            h = abs(self.walk_to(j) / d(i, j))  # 启发式函数
            t = Tau[i, j]  # 信息素浓度
            P.append(t ** alpha * h ** beta)
        P = np.array(P)
        if sum(P) == 0:
            j = np.random.choice(allow)
        else:
            P = P / sum(P)
            j = np.random.choice(allow, p=P)

        # 修改信息
        b = self.walk_to(j)
        self.path.append(j)
        self.t_list.append(self.t + d(i, j))
        self.t += d(i, j) + td * abs(b)
        self.q += abs(b)
        self.C += b  # 更新车上的车辆数
        self.buf[j] -= b  # 更新当前小区调度后的车辆数

    def walk_to(self, j):  # 试着走到j小区，看看装卸量会是怎样？
        i = self.path[-1]
        t_arrive = self.t + d(i, j)  # 到达j的时间
        buf = xu.change_buf(self.buf, self.t_list[-1], t_arrive)
        need = xu.get_requirement(buf, t_arrive)[j]
        if need < 0:  # 小区缺车的情况
            b = max(-self.C, need)
        else:  # 小区多车的情况
            b = min(C_max - self.C, need, ceil(buf[i]))
        return b


if __name__ == '__main__':

    # 定义部分参数
    m = 100  # 蚂蚁数量
    iteration = 0  # 迭代次数初值
    iter_max = 100  # 最大迭代次数

    alpha = 0.1  # 信息素重要程度因子
    beta = 0.1  # 启发函数重要程度因子
    rho = 0.1  # 信息素挥发因子
    Q = 0.1  # 常系数
    times = 1
    while alpha <= 10:
        beta = 0.1
        while beta <= 10:
            rho = 0.1
            while rho <= 10:
                Q = 0.1
                while Q <= 10:
                    q_best = []  # 每代最大Q值
                    q_ave = []  # 每代平均Q值
                    path_best = []  # 每代最优路径
                    iteration = 0
                    # 开始迭代
                    while iteration < iter_max:
                        print('---第%d代---' % (iteration + 1))
                        Path = []  # 记录各个蚂蚁的路径
                        q_list = []  # 记录各个蚂蚁的Q

                        # 产生m只蚂蚁，一一行走
                        for i in range(m):  # 每只蚂蚁一一行走
                            ant = Ant()  # 产生一只蚂蚁，并完成行走
                            Path.append(ant.path)  # 记录这只蚂蚁的路径
                            q_list.append(ant.q)  # 记录这只蚂蚁的Q值

                        # 统计这一代蚂蚁的情况
                        q_ave.append(np.mean(q_list))
                        max_q = max(q_list)
                        max_idx = np.argmax(q_list)
                        if iteration == 0:
                            q_best.append(max_q)
                            path_best.append(Path[max_idx])
                        else:
                            MAX_Q = max(q_best[-1], max_q)
                            if MAX_Q == max_q:
                                q_best.append(max_q)
                                path_best.append(Path[max_idx])
                            else:
                                q_best.append(q_best[-1])
                                path_best.append(Path[-1])

                        # 显示结果
                        print('best q:', q_best[iteration])
                        print('ave:', q_ave[iteration])
                        print('path:', path_best[iteration])

                        # 更新信息素
                        Delta_Tau = np.zeros((n, n))
                        for i in range(m):
                            path, q = Path[i], q_list[i]
                            for j in range(len(path) - 1):
                                Delta_Tau[path[j], path[j + 1]] += q * Q

                        Tau = (1 - rho) * Tau + Delta_Tau
                        iteration = iteration + 1
                        print('')
                    x = np.arange(iter_max) + 1

                    plt.figure(times)
                    plt.plot(x, q_ave)
                    plt.plot(x, q_best)
                    plt.xlabel(('alpha', alpha, 'beta', beta, 'rho', rho, 'Q', Q))
                    plt.savefig('./change/' + str(times) + '.png')
                    times += 1
                    print((Q, ' ', rho, ' ', beta, ' ', alpha, ' ', times))
                    Q += 1
                rho += 1
            beta += 1
        alpha += 1

    plt.show()
