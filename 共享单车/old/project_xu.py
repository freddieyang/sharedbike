import bike
import numpy as np
import random
import matplotlib.pyplot as plt
import visualization_xu as xu


C_max = 20  # 车的容量
d = bike.d  # d(i, j)表示i到j的距离
B = bike.B  # B(i, t)表示i点在t时刻的需求量
T = 60  # 时间限制
td = 0.2  # 装卸一辆车的时间


# 修补一个个体或种群
def repair(x):
    # 个体修补函数
    def repair_one(a):
        for i in range(len(a)):
            a[i] = (a[i] - 2) % 4 + 2  # 修补越界的
        for i in range(1, len(a) - 1):
            while a[i] in (a[i - 1], a[i + 1]):
                a[i] = np.random.randint(2, 6)
        return a

    if x.ndim == 1:  # 若x是一个个体
        return repair_one(x)
    else:  # 若x是一个种群
        for i in range(x.shape[0]):
            x[i] = repair_one(x[i])

    return x


Q = xu.show_detail


class Project(object):

    # 初始化, NP-种群规模, D-维数, Gr-代数, F-缩放因子, Cr-杂交概率
    def __init__(self, NP, D, Gr, F, Cr):
        self.NP = NP  # 种群规模(个体数)
        self.D = D  # 个体维度
        self.Gr = Gr  # 迭代次数
        self.x = np.random.randint(2, 6, (self.NP, self.D))  # 初始化种群矩阵
        self.x = repair(self.x)  # 得修补一下
        self.F = F  # 缩放因子
        self.Cr = Cr  # 杂交概率

    # 变异
    def vary(self):
        def set_r():
            r = np.zeros((self.NP, 3), dtype=int)
            for i in range(r.shape[0]):
                r[i] = random.sample(range(self.NP), 3)
            return r[:, 0], r[:, 1], r[:, 2]

        r1, r2, r3 = set_r()  # 随机生成三个列向量
        v = self.x[r1] + self.F * (self.x[r2] - self.x[r3])  # 变异
        v = np.round(v).astype(int)  # 四舍五入取整
        v = repair(v)  # 修补
        return v

    # 杂交
    def cross(self, v):
        x = self.x
        b = np.random.rand(self.NP, self.D) < self.Cr
        for i in range(self.NP):
            j_rand = np.random.randint(0, self.D)
            b[i][j_rand] = True

        u = b * v + (1 - b) * x
        u = repair(u)
        return u

    # 选择
    def select(self, u):
        for i in range(self.NP):
            if Q(u[i]) > Q(self.x[i]):
                self.x[i] = u[i]

        return self.x

    # 展示这一代种群
    def show_x(self, it, hide=False):
        if not hide:
            print('第%d代种群:' % (it + 1))
        lst = []
        for i in range(self.NP):
            a = self.x[i]
            q, l = Q(a, mode='QL')
            lst.append(q)
            if not hide:
                print(a[:l], q)
        self.y.append(lst)
        if not hide:
            print('')

    # 运行
    def run(self, hide=False):
        self.y = []
        self.show_x(-1, hide=hide)
        if hide:
            print('computing...')
        for it in range(self.Gr):  # 迭代Gr次
            v = self.vary()  # 变异
            u = self.cross(v)  # 杂交
            self.select(u)  # 选择
            self.show_x(it, hide=hide)  # 展示这一代种群

    def plot(self):
        x = [i for i in range(self.Gr + 1)]
        y1 = [max(self.y[i]) for i in range(self.Gr + 1)]
        y2 = [np.mean(self.y[i]) for i in range(self.Gr + 1)]
        plt.plot(x, y1, color='blue')
        plt.plot(x, y2, color='red')
        print('最大值:', y1[-1], ' 平均值:', y2[-1])
        print('达到最大值代数:', y1.index(y1[-1]))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.title('平均调度量和最大调度量')
        plt.show()


if __name__ == '__main__':
    # NP-种群规模, D-维数, Gr-代数, F-缩放因子, Cr-杂交概率
    p = Project(NP=30, D=15, Gr=100, F=1, Cr=0.6)
    p.run(hide=True)  # hide表示是否隐藏每一代的种群信息
    p.plot()
