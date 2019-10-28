import numpy as np
import random


# 交换字符串的第i个字符和第j个字符，返回交换后的字符串
def str_swap(s, i, j):
    s = list(s)
    s[i], s[j] = s[j], s[i]
    s = "".join(s)
    return s


def repair(self, arr):
    for i in range(0, self.path_length):
        arr[0][i] = (arr[0][i] - 2) % 4 + 2
    for i in range(1, self.path_length - 1):
        a = arr[0][i - 1]
        b = arr[0][i + 1]
        while arr[0][i] in [a, b]:
            arr[0][i] = np.random.randint(2, 6)

    return arr


def get_index_xu(x):  # 演化算法用来获得三个随机向量
    r = np.random.randint(0, x, (3, x))
    return r[0, :], r[1, :], r[2, :]


def get_index_yang(x):  # 演化算法用来获得三个随机向量
    index1 = np.argsort(np.random.random_sample((1, x)))
    index2 = np.argsort(np.random.random_sample((1, x)))
    index3 = np.argsort(np.random.random_sample((1, x)))
    r1 = index1
    r2 = index2
    r3 = index3
    return r1, r2, r3


if __name__ == '__main__':
    a = [1.1, 2.8]
    print(np.ceil(a).astype(int).tolist())
