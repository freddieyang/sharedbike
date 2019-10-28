import numpy as np
import math

C_max = 20  # 车的容量
T = 60  # 时间限制
td = 0.2  # 装卸一辆车的时间


# 求两个小区的距离
def d(i, j):
    mat = np.array([[0, 6, 12, 10, 5],
                    [6, 0, 8, 7, 6],
                    [12, 8, 0, 4, 7],
                    [10, 7, 4, 0, 5],
                    [5, 6, 7, 5, 0]])

    return mat[i - 1, j - 1]


def B(point, t):
    def B1(t):
        return 0

    def B2(t):
        if t < 15:
            return -30
        elif t < 60:
            return math.ceil(2 / 3 * t - 40)
        else:
            return 0

    def B3(t):
        if t < 36:
            return -10
        elif t < 60:
            return math.ceil(5 / 12 * t - 25)
        else:
            return 0

    def B4(t):
        if t < 15:
            return math.ceil(10 + 4 / 3 * t)
        else:
            return 30

    def B5(t):
        if t < 15:
            return math.ceil(10 + t)
        else:
            return 25

    Bs = (B1, B2, B3, B4, B5)
    return Bs[point - 1](t)


def E(point, t):
    def E1(t):
        return 0

    def E2(t):
        if t < 15:
            return -30
        elif t < 60:
            return math.ceil(2 / 3 * t - 40)
        else:
            return 0

    def E3(t):
        if t < 36:
            return -10
        elif t < 60:
            return math.ceil(5 / 12 * t - 25)
        else:
            return 0

    def E4(t):
        if t < 15:
            return math.ceil(10 + 4 / 3 * t)
        else:
            return 30

    def E5(t):
        if t < 15:
            return math.ceil(10 + t)
        else:
            return 25

    Es = (E1, E2, E3, E4, E5)
    return Es[point - 1](t)


if __name__ == '__main__':
    print('hello world!')
