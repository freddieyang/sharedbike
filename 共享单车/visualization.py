import bike
import numpy as np
from math import ceil

C_max = bike.C_max  # 车的容量
d = bike.d  # d(i, j)表示i到j的距离
B = bike.B  # B(i, t)表示i点在t时刻的需求量
T = bike.T  # 时间限制
td = bike.td  # 装卸一辆车的时间


# 若a是str或list，转换成ndarray
def transform(a):
    if isinstance(a, list):  # 若a是个list，转换成numpy里面的ndarray
        a = np.array(a)
    elif isinstance(a, str):  # 若a是个字符串，转换成numpy里面的ndarray
        a = np.array([int(c) for c in a])
    return a


# buf0是t1的各小区车辆数，返回t2时刻的车辆数
def change_buf(buf0, t1, t2):
    buf = buf0.copy()
    buf[2] -= (t2 - t1) * 2 / 3
    buf[3] -= (t2 - t1) * 5 / 12
    buf[4] += (t2 - t1) * 2 / 3
    buf[5] += (t2 - t1) * 1 / 2
    if buf[2] < 0:
        buf[2] = 0
    if buf[3] < 0:
        buf[3] = 0
    return buf


# 根据当前时刻、各小区车辆数，得到各小区的车辆需求
def get_requirement(buf, t):
    need_list = [-1, 0, 0, 0, 0, 0]
    need_list[2] = ceil(buf[2] - 2 / 3 * (60 - t))
    need_list[3] = ceil(buf[3] - 5 / 12 * (60 - t))
    need_list[4] = ceil(buf[4] + 2 / 3 * (60 - t) - 20)
    need_list[5] = ceil(buf[5] + 1 / 2 * (60 - t) - 15)
    return need_list


# 展示路径a的详细信息，路径a可以是list、str、ndarray
def show_detail(a, T_limit=T, output=False, mode='Q', visual=False):
    a = transform(a)  # 若a是str或者list，转换为ndarray
    buf = [-1, 0, 10, 15, 10, 10]  # 各个小区有几辆车
    l = 0  # 有效路径长度
    q = 0  # 计算出的Q值, 用于评估a的适应度
    C = 0  # 一开始车是空的
    j = 0  # 一开始车来到a中第一个小区
    t = d(1, a[0])  # 从抵达a中第一个小区的时刻开始
    t_list = [0]  # 记下抵达每个小区的时间，用于更新小区车的数量时计算时间间隔
    t_final = 0  # 抵达最后一个小区的时间
    info = []  # 各小区信息，三维
    global1 = []  # 全局信息，二维
    while t < T_limit:
        t_final = t
        l += 1
        i = a[j]  # i是当前小区的编号
        t_list.append(t)
        if output:
            print('%d、小区%d  时间:%.1f' % (j + 1, i, t), end='  ')

        # 调度前的各小区信息
        info_layer = []
        buf = change_buf(buf, t_list[j], t_list[j + 1])  # 更新每个小区车辆数
        info_layer.append(np.ceil(buf).astype(int).tolist())
        info_layer.append(get_requirement(buf, t))
        info.append(info_layer)

        # 调度前的全局信息
        global1_layer = list()
        global1_layer.append(t)
        global1_layer.append(q)
        global1_layer.append("arrived")
        global1_layer.append("arrived")
        global1_layer.append(C)
        global1.append(global1_layer)

        # 计算需求量，进行调度
        need = get_requirement(buf, t)[i]
        if output:
            print('需求量:%+d' % need, end='  ')
        if need < 0:  # 小区缺车的情况
            b = max(-C, need)
        else:  # 小区多车的情况
            b = min(C_max - C, need, ceil(buf[i]))
        C += b  # 更新车上的车辆数
        buf[i] -= b  # 更新当前小区调度后的车辆数
        if output:
            print('小区的车:%d->%d  车容量%d->%d  调度量:%+d' %
                  (ceil(buf[i] + b), ceil(buf[i]), C - b, C, b), end='  ')
        q += abs(b)  # 更新Q值

        # 调度后的全局信息
        global1_layer = list()
        global1_layer.append(t + td * abs(b))
        global1_layer.append(q)
        global1_layer.append(str(C - b) + '->' + str(C))
        global1_layer.append(str(ceil(buf[i] + b)) + '->' + str(ceil(buf[i])))
        global1_layer.append(C)
        global1.append(global1_layer)

        # 调度后的各小区信息
        info_layer = []
        buf1 = change_buf(buf, t_list[j + 1], t_list[j + 1] + td * abs(b))
        info_layer.append(np.ceil(buf1).astype(int).tolist())
        info_layer.append(get_requirement(buf1, t + td * abs(b)))
        info.append(info_layer)

        if j + 1 >= len(a):  # 可别越界了
            break
        t = t + td * abs(b) + d(a[j], a[j + 1])
        j += 1
        if output:
            print('')

    if output:
        print('\nQ: %d' % q)
        buf = change_buf(buf, t_final, 60)
        print([int(round(buf[i])) for i in range(1, 6)])

    if visual:  # 用于输出可视化信息
        return global1, info
    elif mode == 'QL':  # 用于输出Q和L(有效长度)
        return q, l
    else:  # 用于计算Q
        return q


if __name__ == '__main__':
    path1 = '15243425'
    path2 = '15243245'
    path3 = '15252525'
    show_detail(path2, output=True)

    global1, info = show_detail(path1, visual=True)
    print(np.array(global1).shape)
    print(np.array(info).shape)
    print(global1)
    print(info)
