import numpy as np


def get_random_willing():
    r0 = 0
    r1 = np.random.randint(0, 100 - r0)
    r2 = np.random.randint(0, 100 - (r0 + r1))
    r3 = np.random.randint(0, 100 - (r0 + r1 + r2))
    r4 = np.random.randint(0, 100 - (r0 + r1 + r2 + r3))
    r5 = 100 - (r0 + r1 + r2 + r3 + r4)  # 表示离开区域的概率
    return r0 / 100, r1 / 100, r2 / 100, r3 / 100, r4 / 100, r5 / 100


transfer_matrix = np.array([[0, 0, 0, 0, 0],
                            [0, 0.8, 0.06, 0.03, 0.11],
                            [0, 0.1, 0.75, 0.05, 0.1],
                            [0, 0.2, 0.1, 0.5, 0.2],
                            [0, 0.15, 0.1, 0.15, 0.6]])


# 求两个小区的距离(以自行车的速度)
def d(i, j):
    mat = np.array([[0, 6, 12, 10, 5],
                    [6, 0, 8, 7, 6],
                    [12, 8, 0, 4, 7],
                    [10, 7, 4, 0, 5],
                    [5, 6, 7, 5, 0]])

    return mat[i - 1, j - 1]


vector_init_bike = [0, 10, 15, 10, 10]  # 表示在每个区域的初始化车辆个数
edge_total = 5
bike_total = 200  # 整个区域的车辆
bike_in_vector_total = np.sum(vector_init_bike)  # 表示在区域内的车辆数目

position_list = [0, 1, 2, 3, 4, -1]  # 区域编号，-1表示区域外

bike_out_total = [0, 1, 1, 1, 1]  # 记录每个区域每分钟出入车辆数目


class Edge(object):
    def __init__(self, start, destination):
        self.start = start
        self.destination = destination
        self.bike = []
        self.bike_amount = 0

    def add_bike(self, bike):
        for i in range(len(bike)):
            self.bike.append(bike[i])
            self.bike_amount += 1


class Vector(object):
    def __init__(self, num):
        self.num = num
        self.vector_type = -1  # 0 出行小区，1表示到达小区
        self.bike = []
        self.bike_amount = 0

    def add_bike(self, bike):
        for i in range(len(bike)):
            self.bike.append(bike[i])
            self.bike_amount += 1

    def delete_bike(self, bike):
        self.bike = list(set(self.bike).difference(bike))

    def set_vector_type(self, vector_type):
        self.vector_type = vector_type

    def get_vector_type(self):
        return self.vector_type

    def get_bike(self):
        return self.bike

    def get_num(self):
        return self.num


class Bike(object):
    def __init__(self, num):
        self.num = num
        self.position = -1  # -1表示不在区域中，而在区域外，其他数字表示在某一个区域，也可能是边
        self.next_position = -1  # -1表示不在区域中，而在区域外
        self.willing = get_random_willing()
        self.trace = []
        self.arrive_time = 0
        self.bike_status = 0  # 表示当前车辆的状态，1表示正在去往另一个区域的过程中，0表示其他

    def set_position(self, position):
        self.position = position

    def set_next_position(self, next_position):
        self.next_position = next_position

    def set_bike_status(self, bike_status):
        self.bike_status = bike_status

    def set_arrive_time(self, arrive_time):
        self.arrive_time = arrive_time

    def set_bike_status(self, bike_status):
        self.bike_status = bike_status

    def add_trace(self, trace):
        self.trace.append(trace)

    def get_bike_status(self):
        return self.bike_status

    def get_willing(self):
        return self.willing

    def get_position(self):
        return self.position

    def get_next_position(self):
        return self.next_position

    def get_arrive_time(self):
        return self.arrive_time

    def get_trace(self):
        return self.trace


class Project(object):
    def __init__(self, T):
        self.T = T
        self.out_bikes = []  # 出行单车
        self.in_bike = []  # 到达单车
        self.vector_list = [Vector(i) for i in range(5)]  # 初始化区域列表
        self.edge_list = []
        for i in range(edge_total):
            for j in range(edge_total):
                if i != j:
                    self.edge_list.append(Edge(i, j))
        # self.edge_list = [Edge(i, j) for i in range(edge_total) for j in range(edge_total)]  # 初始化边集
        self.vector_list[1].set_vector_type(0)  # 出行区域
        self.vector_list[2].set_vector_type(0)  # 出行区域
        self.vector_list[3].set_vector_type(1)  # 到达区域
        self.vector_list[4].set_vector_type(1)  # 到达区域
        self.bike_list = [Bike(i) for i in range(bike_total)]  # 初始化总车辆列表
        self.bike_in_vector_list = np.random.choice(self.bike_list, bike_in_vector_total,
                                                    False).tolist()  # 初始化在区域内车辆列表
        self.bike_out_vector_list = list(set(self.bike_list).difference(set(self.bike_in_vector_list)))  # 初始化区域外列表
        temp_bike_list = self.bike_in_vector_list
        for i in range(len(self.vector_list)):
            temp_bike = np.random.choice(temp_bike_list, vector_init_bike[i], False).tolist()
            for item in temp_bike:
                item.set_position(i)
            self.vector_list[i].add_bike(temp_bike)
            temp_bike_list = list(set(temp_bike_list).difference(set(temp_bike)))
        for temp_bike in self.bike_list:
            temp_bike.add_trace(temp_bike.get_position())

    def update(self):
        # 得到每一辆车想去的另一个节点
        for item in self.bike_list:
            # 如果车辆不在行驶中，则更新
            if item.get_bike_status() != 1:
                willing = item.get_willing()
                item.set_next_position(np.int(np.random.choice(position_list, 1, False, willing)))
                # np.int(np.random.choice(position_list, 1, False, transfer_matrix[item.get_position()])))
        self.bike_out()

    # 进入车辆
    def bike_in(self):
        for vector in self.vector_list:
            if vector.get_vector_type() == 1:
                for item in self.bike_out_vector_list:
                    if item.get_next_position() == vector.get_num():
                        pass

    # 外出车辆
    def bike_out(self):
        # 选择将出行区域中的车辆加入到out_bike中，并将想要去另一个区域的车辆加入到边集
        for vector in self.vector_list:
            if vector.get_vector_type() == 0:
                all_bike = vector.get_bike()
                bike_want_to_go_out = []
                # 筛选出想要出去的车
                for bike in all_bike:
                    if bike.get_position() != bike.get_next_position():
                        bike_want_to_go_out.append(bike)
                bike_temp = np.random.choice(bike_want_to_go_out,
                                             bike_out_total[vector.get_num()]).tolist()  # 记录每分钟每个节点有几辆车出此节点
                for bike in bike_temp:
                    # 若车不去区域外并且想去另一个区域
                    if bike.get_next_position() != -1:
                        for edge in self.edge_list:
                            if edge.start == bike.get_position() and edge.destination == bike.get_next_position():
                                edge.add_bike([bike])
                                vector.delete_bike([bike])
                                self.out_bikes.append(bike)
                                bike.set_arrive_time(self.T)
                                bike.set_bike_status(1)
                                bike.set_position(edge)
                                bike.add_trace(('(%d，%d)' % (edge.start, edge.destination)))
                                break
                    else:
                        self.out_bikes.append(bike)


if __name__ == '__main__':
    p = Project(60)
    p.update()
