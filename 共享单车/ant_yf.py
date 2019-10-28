import bike
from math import ceil
import numpy as np
import visualization as vi
import matplotlib.pyplot as plt
from heapq import heappush

C_max = bike.C_max  # 车的容量
d = bike.d  # d(i, j)表示i到j的距离
B = bike.B  # B(i, t)表示i点在t时刻的需求量
T = bike.T  # 时间限制
td = bike.td  # 装卸一辆车的时间

# 定义部分参数
m = 100  # 蚂蚁数量
iter_max = 200  # 最大迭代次数

# alpha_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 信息素重要程度因子
# beta_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 启发函数重要程度因子
# rho_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 信息素挥发因子
# Q_list = [0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]  # 常系数

dim = 15
n = 6
Tau = np.ones((n, n))


class Ant:
    def __init__(self):
        self.path = np.zeros((1, dim))[0].astype(int)
        # self.test = np.array([1, 5, 2, 4, 3, 2, 5, 4]).astype(int)
        self.q = 0
        self.t = 0
        self.C = 0
        self.b = 0
        self.t = 0
        self.buf = [-1, 0, 10, 15, 10, 10]
        self.path[0] = 1
        self.n = n

    def walk(self):
        for i in range(0, len(self.path)):
            # 不能走向自己以及1节点
            allow = list(set([1, 2, 3, 4, 5]).difference([self.path[i]]).difference([1]))
            for item in allow:
                if self.t + d(item, self.path[i]) > T:
                    allow = list(set(allow).difference([item]))
            if len(allow) == 0:
                break
            P = np.zeros((1, len(allow)))[0]
            for j in range(len(allow)):
                n = self.try_walk(self.path[i], allow[j]) / d(self.path[i], allow[j])
                t = Tau[self.path[i], allow[j]]
                P[j] = t ** alpha * n ** beta
            if sum(P) == 0:
                P = np.ones((1, len(allow)))
            P = P / sum(P)
            # 轮盘赌法选择下一个访问城市
            PC = np.cumsum(P)
            target = allow[np.array(np.where(PC > np.random.random()))[0][0]]
            self.try_walk(self.path[i], target, True, i + 1)
        # 测试
        # self.q = 0
        # self.t = 0
        # self.C = 0
        # self.b = 0
        # self.buf = [-1, 0, 10, 15, 10, 10]
        # for index in range(1, len(self.test)):
        #     self.try_walk(self.test[index - 1], self.test[index], True)

    def try_walk(self, start, destination, flag=False, i=0):
        temp_t = self.t
        t1 = temp_t
        temp_t = self.t + d(start, destination)
        t2 = temp_t
        temp_buf = self.buf
        temp_buf = vi.change_buf(temp_buf, t1, t2)
        need = vi.get_requirement(temp_buf, temp_t)[destination]
        if need < 0:  # 小区缺车的情况
            temp_b = max(-self.C, need)
        else:  # 小区多车的情况
            temp_b = min(C_max - self.C, need, ceil(temp_buf[destination]))
        if flag:
            self.b += temp_b
            t3 = temp_t
            self.t = temp_t + abs(temp_b) * td
            t4 = self.t
            self.buf[destination] -= temp_b
            self.buf = vi.change_buf(self.buf, t3, t4)
            if self.buf[destination] < 0:
                self.buf[destination] = 0
            self.C += temp_b
            self.path[i] = destination
            self.q += abs(temp_b)
        return abs(temp_b)


if __name__ == '__main__':
    # 运行多次
    times = 50
    for time in range(times):
        # 迭代
        q_best = []
        q_ave = []
        total_best = []
        path_best = []

        Tau = np.ones((n, n))

        alpha = 2
        beta = 1
        rho = 0.05
        Q = 0.000036
        for i in range(iter_max):
            Path = []
            Ants = []
            q_list = []

            for j in range(m):
                ant = Ant()
                ant.walk()
                Ants.append(ant)
                q_list.append(ant.q)
                Path.append(ant.path)

            Delta_Tau = np.zeros((n, n))
            for t in range(m):
                path, q = Path[t], q_list[t]
                for j in range(len(path) - 1):
                    if path[j + 1] == 0:
                        break
                    Delta_Tau[path[j], path[j + 1]] += q * Q
            Tau = (1 - rho) * Tau + Delta_Tau
            q_best.append(np.max(q_list))
            q_ave.append(np.average(q_list))
            total_best.append(np.max(q_best))
            path_best.append(Path[np.argmax(q_best)])

        # 绘图
        print('第', time + 1, '次')
        print('最大调度量：', max(total_best))
        print('平均调度量：', np.mean(q_ave))
        x = np.arange(iter_max) + 1
        plt.figure(time)
        plt.plot(x, q_ave, color='red')
        plt.plot(x, total_best, color='blue')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.title('平均调度量和最大调度量')
        plt.xlabel(('alpha: ', alpha, 'beta: ', beta, 'rho: ', rho, 'Q: ', Q))
        plt.savefig('./save/' + str(time) + '.png')

    plt.show()
