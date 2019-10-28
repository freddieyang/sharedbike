import matplotlib.pyplot as plt
import numpy as np
import visualization_xu as vx
import matplotlib.patches as patches

x = [2, 1.25, 2.75, 1.6, 2.4]
y = [3, 2.25, 2.25, 1.25, 1.25]

path = np.array([1, 5, 2, 4, 3, 4, 2, 5])
global1, info = vx.show_detail(path, visual=True)
index = ['a', 'b', 'c', 'd', 'e']
for layer in range(len(global1)):
    fig, ax = plt.subplots()

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    plt.xticks([])
    plt.yticks([])

    idx = path[layer // 2] - 1
    for i in range(len(x)):
        if i != idx:
            plt.scatter(x[i], y[i], color='b')
        else:
            plt.scatter(x[i], y[i], color='r')
            plt.scatter(x[i] + 0.05, y[i], color='w')
            currentAxis = plt.gca()
            rect = patches.Rectangle(
                (x[i] + 0.05, y[i]), 0.15, 0.2, linewidth=1, edgecolor='r',
                facecolor='none')
            currentAxis.add_patch(rect)
            plt.annotate((str(global1[layer][4])), (x[i], y[
                         i]), xytext=(x[i] + 0.1, y[i] + 0.04))
        plt.annotate((i + 1), (x[i], y[i]), xytext=(x[i] - 0.01, y[i] + 0.1))
        currentAxis = plt.gca()
        rect = patches.Rectangle(
            (x[i] - 0.1, y[i] - 0.43), 0.3, 0.35, linewidth=1, edgecolor='none',
            facecolor='none')
        currentAxis.add_patch(rect)
        plt.annotate(('Cars: ' + str(info[layer][0][i + 1])), (x[i], y[i]),
                     xytext=(x[i] - 0.1, y[i] - 0.2))

        plt.annotate(('Needs: ' + str(info[layer][1][i + 1])), (x[i], y[i]),
                     xytext=(x[i] - 0.1, y[i] - 0.35))
        plt.title('T = ' + str(global1[layer][0]) +
                  '   Q = ' + str(global1[layer][1]))
    plt.axis([1, 3, 0, 3.5])
    if layer != 0 and layer != 1:
        plt.plot([x[path[layer // 2 - 1] - 1], x[path[layer // 2] - 1]],
                 [y[path[layer // 2 - 1] - 1], y[path[layer // 2] - 1]],
                 color='r')
    # plt.savefig('./save/' + str(layer + 1) + '.png')


def update(times):
    # for i in range(len(x)):
    #     plt.scatter(a[i], b[i], color='b')
    # plt.plot([x[0], x[1]], b[1], color='r')
    # plt.close('all')
    # fig=plt.figure(times)
    print(times)
    plt.scatter([x[path[times] - 1], x[path[times + 1] - 1]], [y[path[times] - 1], y[path[times + 1] - 1]],
                color='r')
    plt.scatter([x[path[times - 1] - 1], x[path[times] - 1]], [y[path[times - 1] - 1], y[path[times] - 1]],
                color='b')
    for i in range(len(x)):
        pass
    # plt.plot([x[path[times - 1] - 1], x[path[times] - 1]], [y[path[times - 1] - 1], y[path[times] - 1]], color='w')
    plt.plot([x[path[times] - 1], x[path[times + 1] - 1]],
             [y[path[times] - 1], y[path[times + 1] - 1]], color='r')
    # plt.annotate(' ', (x[path[times] - 1], y[path[times] - 1]))
    plt.annotate(path[times + 1],
                 (x[path[times + 1] - 1], y[path[times + 1] - 1]))
    ax.set_xlabel(('T = ' + str(global1[times + 1][0]), 'Q = ' + str(global1[times + 1][1]),
                   'Car = ' + str(global1[times + 1][2]
                                  ), 'At = ' + str(global1[times + 1][3]),
                   'Ci = ' + str(global1[times + 1][4])))
    plt.axis([1, 3, 1, 3.5])


if __name__ == '__main__':
    plt.show()

# animation = FuncAnimation(fig, update, frames=np.arange(len(path) - 1), interval=2000)
# plt.show()


# Recycle Bin
# a = [[x[1], x[2]], [x[1], x[3]], [x[1], x[4]], [x[1], y[5]], [x[2], x[3]], [x[2], x[4]], [x[2], x[5]], [x[3], x[4]],
#      [x[3], x[5]], [x[4], x[5]]]
# b = [[y[1], y[2]], [y[1], y[3]], [y[1], y[4]], [y[1], y[5]], [y[2], y[3]], [y[2], y[4]], [y[2], y[5]], [y[3], y[4]],
#      [y[3], y[5]], [y[4], y[5]]]
