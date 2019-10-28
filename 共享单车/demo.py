import numpy as np
import bike

init = np.array([0, 0.2, 0.3, 0.4, 0.1])
m = init.shape[0]  # m个小区
transfer_matrix = np.array([[0, 0, 0, 0, 0],
                            [0, 0.8, 0.06, 0.03, 0.11],
                            [0, 0.1, 0.75, 0.05, 0.1],
                            [0, 0.2, 0.1, 0.5, 0.2],
                            [0, 0.15, 0.1, 0.15, 0.6]])

d = bike.d  # 各小区之间的骑行时间


# 类，表示一辆单车
class Bike(object):

    # 初始化单车，单车位置随机
    def __init__(self):
        self.at = np.random.choice(range(m), p=init)
        self.trace = [self.at]
        self.stay = [0]  # 单车在trace上每个地点停留的时间
        self.clk = 0  # 还有多少时间到达下一个地点。0意味着已经停在某个地点
        # self.moving = False  # 这辆单车是否在路上

    # 推算该单车t分钟后的位置信息
    def next(self, t=1):
        for i in range(t):
            if self.clk > 0:
                self.clk -= 1
            else:
                aim = np.random.choice(range(m), p=transfer_matrix[self.at])
                if aim != self.at:
                    self.clk = d(self.at, aim) - 1
                    self.at = aim
                    self.trace.append(aim)
                    self.stay.append(0)
                else:
                    self.stay[-1] += 1

    # 显示单车行进路线
    def show_trace(self):
        if self.clk > 0:
            bound = len(self.trace) - 1
        else:
            bound = len(self.trace)
        print('[', end='')
        for i in range(bound):
            if i != 0:
                print(' ', end='')
            if self.stay[i] == 0:
                print('%d' % self.trace[i], end='')
            else:
                print('%d(%d)' % (self.trace[i], self.stay[i]), end='')
        print(']', end=' ')
        if self.clk > 0:
            print('正在前往%d' % self.at)
        else:
            print('停在了%d' % self.at)


class Project(object):

    # 创建n辆自行车，并移动t分钟
    def __init__(self, n, t):
        self.n = n
        self.t = t
        self.bikes = [Bike() for i in range(n)]  # 创建自行车群
        for i in range(n):
            self.bikes[i].next(t)

    # 统计每个小区有多少辆车
    def count(self):
        self.ans = [0 for i in range(m)]
        for i in range(self.n):
            if self.bikes[i].clk == 0:
                self.ans[self.bikes[i].at] += 1
        print('停在各小区的一共有 %d 辆' % sum(self.ans))
        for j in range(m):
            print('小区%d:%d辆' % (j, self.ans[j]), end='  ')
        print('')
        return self.ans

    # 展示每一辆自行车的行进路线
    def show_trace(self):
        for i in range(self.n):
            self.bikes[i].show_trace()


# 主函数
if __name__ == '__main__':
    p = Project(n=20, t=60)
    p.show_trace()
    p.count()
