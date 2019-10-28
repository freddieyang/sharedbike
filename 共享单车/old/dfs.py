import bike

C = bike.C_max  # 车的容量
d = bike.d  # d(i, j)表示i到j的距离
B = bike.B  # B(i, t)表示i点在t时刻的需求量
T = bike.T  # 时间限制


class Node(object):

    def __init__(self, parent, i):
        self.i = i
        self.parent = parent
        if parent:
            self.t = parent.t + parent.td + d(parent.i, i)
        else:
            self.t = 0

        if not parent:
            self.is_first = True
        else:
            self.is_first = False

        self.service()

    # 输出到当前节点的路径(递归)
    def print_node(self):
        if self.parent:
            self.parent.print_node()
            print(self.i, self.t, B(self.i, self.t),
                  self.parent.buf[self.i], -self.x, self.C, sep='\t')
        else:
            return

    def print_path(self):
        self.print_node()
        print('')

    # buf表示每个地方的库存
    def service(self):
        if self.is_first:
            self.sum = 0
            self.C = 0
            # buf表示每个站点的累计装卸，+表示获得，-表示失去
            self.buf = [0, 0, 0, 0, 0, 0]
            self.td = 0
            self.x = 0

        else:
            parent = self.parent
            i = self.i
            buf = parent.buf.copy()
            need = B(self.i, self.t) + buf[i]
            x = 0  # x表示装卸量, 恒为正

            # i车辆不足
            if need < 0:
                if abs(need) >= parent.C:
                    x = parent.C
                    buf[i] += x
                    self.C = 0
                else:
                    x = abs(need)
                    buf[i] += x
                    self.C = parent.C - x
            # i车辆过剩
            else:
                if need > C - parent.C:
                    x = C - parent.C
                    buf[i] -= x
                    self.C = C
                else:
                    x = need
                    buf[i] -= x
                    self.C = parent.C + x
            self.sum = parent.sum + x
            self.buf = buf
            self.td = 0.2 * x
            if need < 0:
                self.x = -x
            else:
                self.x = x


def DFS(opt=-1):
    s = []  # 这是一个栈
    max_Q = 0
    node = Node(parent=None, i=1)
    s.append(node)
    while s:
        node = s.pop()
        if node.t > T:
            continue
        else:
            max_Q = max(max_Q, node.sum)
            if opt != -1 and node.sum >= opt:
                node.print_path()
        for i in [2, 3, 4, 5]:
            # 下一个节点不要访问自己
            if i == node.i:
                continue
            new_node = Node(parent=node, i=i)
            # 如果新节点还有时间，那就给他个机会
            if new_node.t <= T:
                s.append(new_node)

    return max_Q


def analysis(path):
    node = Node(parent=None, i=1)
    for j in range(len(path)):
        if path[j] == 1:
            continue
        new_node = Node(parent=node, i=path[j])
        node = new_node

    print(node.sum)
    node.print_path()


if __name__ == '__main__':
    flag = 2

    if flag == 1:  # 找出指定T下的最优解
        max_Q = DFS()
        print(max_Q)
        DFS(max_Q)

    elif flag == 2:  # 判断指定路径下的Q和b
        path1 = [1, 5, 2, 4, 3, 4, 2, 5]
        path2 = [1, 5, 2, 4, 3, 2, 4, 5]
        path3 = [1, 5, 3, 4, 2, 3, 4, 3, 4]
        print('i\tt\tB\tbuf\tb\tCi')
        analysis(path3)

    elif flag == 3:  # 比较不同T下的最大Q值
        for var_t in range(40, 66):
            T = var_t
            max_Q = DFS()
            print('T=%s  Q=%d' % (T, max_Q))
