import numpy as np


def f(x, index):
    if index == 1:
        return np.sum(x ** 2, 1)
    if index == 2:
        return 20 + np.sum(x ** 2, 1) - 10 * np.sum(np.cos(2 * np.pi * x), 1)


class DE:
    def __init__(self, NP, dimension, F, Cr, generation, question_index, lower, upper):
        self.NP = NP
        self.dimension = dimension
        self.F = F
        self.Cr = Cr
        self.generation = generation
        self.question_index = question_index
        self.lower = lower
        self.upper = upper
        self.pop = self.init()

    def init(self):
        return self.lower + (self.upper - self.lower) * np.random.random_sample([self.NP, self.dimension])

    def get_index(self):  # 演化算法用来获得三个随机向量
        r = (np.argsort(np.random.randint(0, self.NP, (3, self.NP))).reshape(-1)).reshape((self.NP, 3))
        return r[:, 0], r[:, 1], r[:, 2]

    def new_pop(self):
        r1, r2, r3 = self.get_index()
        vi = (self.pop[r1] + self.F * (self.pop[r2] - self.pop[r3])).reshape((self.NP, self.dimension))
        vi = self.repair(vi)
        j = np.random.random_sample((self.NP, self.dimension)) < self.Cr
        for i in range(0, j.shape[0]):
            j[i][np.random.randint(0, self.dimension)] = True
        ui = j * vi + (1 - j) * self.pop
        better_index = (f(ui, self.question_index) < f(self.pop, self.question_index)).reshape(self.NP, 1)
        self.pop = better_index * ui + (1 - better_index) * self.pop

    def repair(self, vi):
        smaller = vi < lower
        larger = vi > upper
        check = 1 - np.logical_or(smaller, larger)
        tmp_smaller = np.minimum(upper, 2. * lower - smaller * vi) * smaller
        tmp_larger = np.maximum(lower, 2. * upper - larger * vi) * larger
        return vi * check + tmp_larger + tmp_smaller

    def run(self):
        for i in range(self.generation):
            self.new_pop()
            print(i, '--------------------------')
            print(self.pop)


if __name__ == '__main__':
    NP = 30
    dimension = 2
    F = 0.6
    Cr = 0.6
    lower = -1
    upper = 1
    generation = 1000
    question_index = 1
    # print(init(NP, dimension, lower, upper))
    de = DE(NP, dimension, F, Cr, generation, question_index, lower, upper)
    de.run()
