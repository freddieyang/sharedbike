import numpy as np


# 求两个小区的距离(以自行车的速度)
def d(i, j):
    mat = np.array([[0, 6, 12, 10, 5],
                    [6, 0, 8, 7, 6],
                    [12, 8, 0, 4, 7],
                    [10, 7, 4, 0, 5],
                    [5, 6, 7, 5, 0]])

    return mat[i - 1, j - 1]


class Vector(object):

    def __init__(self):
        self.bike = []
        self.bike_amount = 0

    def add_bike(self, bike):
        self.bike.append(bike)
        self.bike_amount += 1


# 表示一辆单车的位置信息
class Position(object):

    def __init__(self, a, b, r=-1):
        self.a = a  # 左端点
        self.b = b  # 右端点
        self.e = (a, b)  # 左右端点
        self.L = d(a, b)  # 长度
        if r == -1:
            self.r = self.L - 1
        else:
            self.r = r


class Bike(object):

    def __init__(self, birth_place):
        self.pos = Position(birth_place, birth_place, 0)

    def show(self):
        print(self.pos.a, self.pos.b)


init = [0, 10, 15, 5, 20]  # 初始每个小区有多少辆车


class Project(object):

    def __init__(self, T):
        self.T = T
        self.bikes = []
        for j, n in enumerate(init):
            for i in range(n):
                bike = Bike(j)
                self.bikes.append(bike)

        self.run(self.T)

    def run(self, T):
        for t in T:  # 每分钟更新一次状态
            buf = [[], [], [], [], []]
            for i, bike in enumerate(self.bikes):
                if bike.pos.r == 0:  # 如果自行车在某小区停着
                    at = bike.pos.b
                    buf[at].append(i)
                else:
                    bike.pos.r -= 1
            # 接下来挑一些车出行


if __name__ == '__main__':
    p = Project(T=60)
