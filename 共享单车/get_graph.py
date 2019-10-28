import matplotlib.pyplot as plt
import numpy as np
import visualization as vx
import matplotlib.patches as patches
# from project import Project as pj

x = [2, 1.25, 2.75, 1.6, 2.4]
y = [3, 2.25, 2.25, 1.25, 1.25]
# a = [[x[0], x[3]], [x[0], x[4]], [x[1], x[2]], [x[1], x[4]], [x[2], x[3]]]
# b = [[y[0], y[3]], [y[0], y[4]], [y[1], y[2]], [y[1], y[4]], [y[2], y[3]]]
# 结构：全局：Q，t，|| 小区：小区现在车辆数，需求车辆，调度量 || 车容量变化

# for i in range(len(a)):
#     plt.plot(a[i], b[i])


path1 = np.array([5, 2, 4, 3, 4, 2, 5])
path = np.array([1, 5, 2, 4, 3, 2, 4, 5])
global1, info = vx.show_detail(path, visual=True)
index = ['A', 'B', 'C', 'D', 'E']
for layer in range(len(global1)):
    fig, ax = plt.subplots()
    idx = path[layer // 2] - 1
    f = 1
    for i in range(len(x)):
        if i != idx:
            plt.scatter(x[i], y[i] + 0.1, edgecolors='black', c='', s=300)
        else:
            plt.scatter(x[i], y[i] + 0.1, edgecolors='black', c='', s=300)
            plt.scatter(x[i] + 0.05, y[i], color='w')
            currentAxis = plt.gca()
            rect = patches.Rectangle((x[i] + 0.07, y[i]), 0.15, 0.2, linewidth=1, edgecolor='r', facecolor='none')
            currentAxis.add_patch(rect)
            plt.annotate((str(global1[layer][4])), (x[i], y[i]), xytext=(x[i] + 0.1, y[i] + 0.07))  # 显示小车上的数
            plt.scatter(x[i] + 0.11, y[i], color='r')
            plt.scatter(x[i] + 0.18, y[i], color='r')
        plt.annotate(index[i], (x[i], y[i]), xytext=(x[i]-0.023 , y[i] + 0.05))
        while f == 1:
            # 显示图例
            plt.annotate('Bikes', (x[i], y[i]),
                         xytext=(x[i] - 0.9, y[i] + 0.2))  # Cars
            plt.annotate('Needs', (x[i], y[i]),
                         xytext=(x[i] - 0.9, y[i]))  # Cars

            # 显示表格
            currentAxis = plt.gca()
            rect = patches.Rectangle((x[i] - 0.91, y[i] - 0.05), 0.2, 0.2, linewidth=1, edgecolor='black',
                                     facecolor='none')
            currentAxis.add_patch(rect)
            currentAxis = plt.gca()
            rect = patches.Rectangle((x[i] - 0.91, y[i] + 0.15), 0.2, 0.2, linewidth=1, edgecolor='black',
                                     facecolor='none')
            currentAxis.add_patch(rect)
            f = 0

        currentAxis = plt.gca()
        rect = patches.Rectangle((x[i] - 0.07, y[i] - 0.43), 0.15, 0.18, linewidth=1, edgecolor='black',
                                 facecolor='none')
        currentAxis.add_patch(rect)
        rect = patches.Rectangle((x[i] - 0.07, y[i] - 0.25), 0.15, 0.18, linewidth=1, edgecolor='black',
                                 facecolor='none')
        currentAxis.add_patch(rect)
        plt.annotate((str(info[layer][0][i + 1])), (x[i], y[i]),
                     xytext=(x[i] - 0.05, y[i] - 0.2))  # Cars

        plt.annotate((str(info[layer][1][i + 1])), (x[i], y[i]),
                     xytext=(x[i] - 0.05, y[i] - 0.4))  # Needs
        ax.set_xlabel('T = ' + str(float(global1[layer][0])) + ' ,  Q = ' + str(global1[layer][1]))
    plt.axis([1, 3, 0, 3.5])
    plt.xticks([])
    plt.yticks([])
    if layer != 0 and layer != 1:
        plt.plot([x[path[layer // 2 - 1] - 1], x[path[layer // 2] - 1]],
                 [y[path[layer // 2 - 1] - 1], y[path[layer // 2] - 1]],
                 color='r')
    if layer != 0:
        plt.savefig('./save/' + str(layer) + '.png')

if __name__ == '__main__':
    plt.show()

# animation = FuncAnimation(fig, update, frames=np.arange(len(path) - 1), interval=2000)
# plt.show()


# Recycle Bin
# a = [[x[1], x[2]], [x[1], x[3]], [x[1], x[4]], [x[1], y[5]], [x[2], x[3]], [x[2], x[4]], [x[2], x[5]], [x[3], x[4]],
#      [x[3], x[5]], [x[4], x[5]]]
# b = [[y[1], y[2]], [y[1], y[3]], [y[1], y[4]], [y[1], y[5]], [y[2], y[3]], [y[2], y[4]], [y[2], y[5]], [y[3], y[4]],
#      [y[3], y[5]], [y[4], y[5]]]
