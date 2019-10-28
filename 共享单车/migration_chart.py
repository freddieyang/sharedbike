import numpy as np
from matplotlib import pyplot as plt

# 五个节点的坐标
x = [2, 1.25, 2.75, 1.6, 2.4]
y = [3, 2.25, 2.25, 1.25, 1.25]

# 马尔可夫链转移函数
transfer_matrix = np.array([[0, 0, 0, 0, 0],
                            [0, 0.2, 0.3, 0.2, 0.3],
                            [0, 0.35, 0.35, 0.1, 0.2],
                            [0, 0.25, 0.1, 0.25, 0.4],
                            [0, 0.2, 0.25, 0.45, 0.1]])


def markov(init_array):
    restmp = init_array
    for i in range(100):
        res = np.dot(restmp, transfer_matrix)
        print(i, "\t", res)
        restmp = res


def init_bike(low, bike_total, community_total, length):
    bike = np.random.randint(low, community_total + 1, [bike_total, length])
    return bike


index = ['A', 'B', 'C', 'D', 'E']


def visualization():
    for i in range(len(x)):
        plt.scatter(x[i], y[i], edgecolors='black', c='', s=300)
        plt.annotate(index[i], (x[i], y[i]), xytext=(x[i] - 0.023, y[i]))
    for i in range(0, transfer_matrix.shape[0]):
        for j in range(0, transfer_matrix.shape[1]):
            plt.plot([x[i], x[j]],
                     [y[i], y[j]], color='r', linewidth=transfer_matrix[i][j] * 2)

    plt.xticks([])
    plt.yticks([])
    plt.show()


if __name__ == '__main__':
    low = 2
    high = 6
    bike_total = 30
    community_total = 5
    length = 15
    # print(init_bike(low, bike_total, community_total, length))
    init_array = np.array([0, 0.2, 0.3, 0.4, 0.1])
    # markov(init_array)
    visualization()
