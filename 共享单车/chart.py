from matplotlib import pyplot as plt

# 五个节点的坐标
x = [25, 0, 50, 0, 50]
y = [75, 50, 50, 0, 0]

index = ['A', 'B', 'C', 'D', 'E']


def visualization():
    for i in range(len(x)):
        plt.scatter(x[i], y[i], edgecolors='black', c='', s=300)
        plt.annotate(index[i], (x[i], y[i]), xytext=(x[i] - 0.023, y[i]))
    plt.xticks([])
    plt.yticks([])
    plt.show()


if __name__ == '__main__':
    visualization()
