import DE as de
import numpy as np
import random
from matplotlib import pyplot
import copy
import bike


class Project:

    def __init__(self, path_amount, path_length, total_time, one_time,
                 C, F, Cr, generation):
        self.C = C  # 车容量
        self.Cr = Cr  # 杂交概率
        self.F = F  # 缩放因子
        self.t = 0  # 用来计算全局时间
        self.true_length = 0  # 暂时不用
        self.one_time = one_time  # 设置每次上下一辆车的时间
        self.total_time = total_time  # 设置总时间
        self.path_length = path_length  # 设置路径最大长度
        self.path_amount = path_amount  # 设置个体维度
        self.generation = generation
        self.path = np.random.randint(
            2, 6, (path_amount, path_length))  # 初始化路径
        self.path = self.repair(np.array(self.path))  # 修补初始化路径
        self.shortest_time = np.array(
            [[0, 6, 12, 10, 5],
             [6, 0, 8, 7, 6],
             [12, 8, 0, 4, 7],
             [10, 7, 4, 0, 5],
             [5, 6, 7, 5, 0]])  # 点到点所需要花费的时间
        self.requirement = np.zeros((1, 5), dtype=int)  # 需求列表初始化
        self.update_requirement()  # 更新需求
        self.best = np.array([0] * generation)

    def B1(self):
        return 0

    def B2(self):

        if self.t < 15:
            return -30
        if self.t < 60:
            return np.ceil(2 / 3 * self.t - 40)
        else:
            return 0

    def B3(self):

        if self.t < 36:
            return -10
        if self.t < 60:
            return np.ceil(5 / 12 * self.t - 25)
        else:
            return 0

    def B4(self):

        if self.t < 30:
            return np.ceil(10 + 2 / 3 * self.t)
        else:
            return 30

    def B5(self):

        if self.t < 30:
            return 10 + np.ceil(0.5 * self.t)
        else:
            return 25

    def repair(self, arr):  # 修补函数
        for i in range(0, len(arr[:, 0])):
            for j in range(0, len(arr[0, :])):
                arr[i][j] = (arr[i][j] - 2) % 4 + 2
            for j in range(1, len(arr[0, :]) - 1):
                while arr[i][j] in [arr[i][j - 1], arr[i][j + 1]]:
                    arr[i][j] = np.random.randint(2, 6)
        return arr

    def update_requirement(self):  # 更新需求所用
        self.requirement[0][0] = self.B1()
        self.requirement[0][1] = self.B2()
        self.requirement[0][2] = self.B3()
        self.requirement[0][3] = self.B4()
        self.requirement[0][4] = self.B5()

    # def get_path(self, arr):
    #     return arr[0:self.true_length]

    def print_path(self, arr):  # 输出路径
        length = 0
        t = self.get_q(np.array([arr]))[0][0] * self.one_time  + self.shortest_time[0][arr[length] - 1]
        while t < self.total_time:
            # if t + self.shortest_time[0][arr[i] - 1] < self.total_time:
            #     length += 1
            #     t += self.shortest_time[0][arr[i] - 1]
            length += 1
            t += self.shortest_time[arr[length - 1] - 1][arr[length] - 1]
        print(arr[0:length], 'Q：', self.get_q(np.array([arr]))[0][0])

    def get_q(self, arr):
        q = np.zeros((1, self.path_amount), dtype=int)
        for index in range(0, arr.shape[0]):
            buf = np.zeros((1, 5), dtype=int)  # 负数表示已经运出去多少，正数表示已经运进来多少
            self.t = 0
            self.true_length = 0  # 记录真实长度
            Ci = 0  # 调度车上面车辆的数目
            bi = 0  # 实际调度量
            # t_tmp = 0
            self.t += self.shortest_time[0][arr[index][0] - 1]  # 增加全局时间
            self.update_requirement()  # 更新需求
            Bi = self.requirement[0][arr[index][0] - 1]  + buf[0][arr[index][0] - 1]  # 调度需求
            if Bi < 0:
                bi = max(-Ci, Bi)
            if Bi > 0:
                bi = min(self.C - Ci, Bi)
            q[0][index] += abs(bi)  # 总调度量
            buf[0][arr[index][0] - 1] -= bi
            Ci += bi  # 车上还剩下的车辆
            self.t += abs(bi) * self.one_time  # 全局时间添加装卸车的用时
            # self.update_requirement() #更新需求
            for i in range(1, len(arr[index])):
                # 判断到哪个停止
                # 将总时间添加从一个地区到达另一个地区的时间
                self.t += self.shortest_time[arr[index][i - 1] - 1][arr[index][i] - 1]
                if self.t < self.total_time:
                    self.update_requirement()
                    Bi = self.requirement[0][arr[index][i] - 1]  + buf[0][arr[index][i] - 1]  # 获得需求
                    if Bi <= 0:
                        bi = max(-Ci, Bi)
                    if Bi > 0:
                        bi = min(self.C - Ci, Bi)
                    q[0][index] += abs(bi)
                    buf[0][arr[index][i] - 1] -= bi
                    Ci += bi
                    self.t += abs(bi) * self.one_time
        return q

    def get_index(self):  # 演化算法用来获得三个随机向量
        r1 = np.array([], dtype=int)
        r2 = np.array([], dtype=int)
        r3 = np.array([], dtype=int)
        for i in range(0, self.path_amount):
            tmp = np.argsort(np.random.random_sample((1, self.path_length)))
            r1 = np.hstack((r1, tmp[0][0]))
            r2 = np.hstack((r2, tmp[0][1]))
            r3 = np.hstack((r3, tmp[0][2]))
        return r1, r2, r3

    def get_index_xu(self):  # 演化算法用来获得三个随机向量
        r = np.random.randint(0, self.path_amount, (3, self.path_amount))
        return r[0, :], r[1, :], r[2, :]

    def new_path(self):  # 演化算法主函数
        r1, r2, r3 = self.get_index()
        vi = (self.path[r1] + self.F * (self.path[r2] - self.path[r3])).reshape((self.path_amount, self.path_length))
        j = np.random.random_sample((self.path_amount, self.path_length)) < self.Cr
        for i in range(0, j.shape[0]):
            j[i][np.random.randint(0, self.path_length)] = True
        ui = j * vi + (1 - j) * self.path
        ui = self.repair(ui)
        l_index = (self.get_q(ui) > self.get_q(self.path)).reshape(self.path_amount, 1)
        tmp = l_index
        for i in range(0, self.path_length - 1):
            l_index = np.hstack((l_index, tmp))
        self.path = l_index * ui + (1 - l_index) * self.path

    def run(self):
        for i in range(self.generation):
            self.new_path()
            print(i, '--------------------------')
            for j in range(0, self.path_amount):
                self.print_path(np.array(self.path[j]))

    def plot(self):
        pass


if __name__ == '__main__':
    p = Project(path_amount=30, path_length=15,
                total_time=60, one_time=0.2, C=20,
                F=1, Cr=0.6, generation=1000)
    # path1 = [5, 2, 4, 3, 2, 4, 5]
    # p.get_q(np.array([path1]))
    p.run()
