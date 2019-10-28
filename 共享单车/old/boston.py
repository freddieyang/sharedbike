from sklearn.datasets import load_boston
import numpy as np


def split_data(x, y, k=0.7):
    data = np.concatenate((x, y), axis=1)
    np.random.shuffle(data)
    t = int(k * x.shape[0])
    x_train = data[:t, :-1]
    y_train = data[:t, -1]
    x_test = data[t:, :-1]
    y_test = data[t:, -1]
    return x_train, y_train, x_test, y_test


def load_data(k=0.7):
    boston = load_boston()
    x = boston.data
    y = boston.target
    y = y.reshape((y.shape[0], 1))
    x_train, y_train, x_test, y_test = split_data(x, y, k=0.7)
    y_train = y_train.reshape((y_train.shape[0], 1))
    y_test = y_test.reshape((y_test.shape[0], 1))
    return x_train, y_train, x_test, y_test


# 主函数，展示了如何读取并划分数据集
if __name__ == '__main__':
    print('——————————读取并划分波士顿房价数据集——————————')
    print('\n\t正在处理 ...')
    x_train, y_train, x_test, y_test = load_data()
    print('\t读取并划分成功！')
    print('\t训练集和测试集的尺寸:')
    print('   ', x_train.shape, y_train.shape, x_test.shape, y_test.shape)
    print('')
    print('------------------- DONE -------------------')
