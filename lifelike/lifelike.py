import numpy as np


class Lifelike:
    def __init__(self, x, y, rule=None):
        self.dim_x = x
        self.dim_y = y
        self.rule  = rule

        self.dim_t = 0

        self.X = np.arange(self.dim_x)
        self.Y = np.arange(self.dim_y)
        self.T = None

        self.U_0 = np.zeros((1, self.dim_x, self.dim_y))
        self.U   = np.zeros((0, self.dim_x, self.dim_y))

    def __repr__(self):
        if self.dim_t == 0:
            return repr(self.U_0[0])
        else:
            return repr(self.U[-1])

    def add_being(self, being, x, y):
        if self.rule == None:
            self.rule = being.rule

        if self.rule == being.rule:
            self.U_0[0][x:x + being.U.shape[0], y:y + being.U.shape[1]] = being.U
        else:
            #TODO Raise exception
            print('Error: Rule mismatch.')

    def add_being_top_left(self, being):
        self.add_being(being, 2, 2)

    def add_being_middle(self, being):
        self.add_being(being, (self.dim_x - being.U.shape[0]) // 2, (self.dim_y - being.U.shape[1]) // 2)

    def add_being_bottom_right(self, being):
        self.add_being(being, self.dim_x - being.U.shape[0] - 4, self.dim_y - being.U.shape[1] - 4)

    def add_being_middle_bottom(self, being):
        self.add_being(being, self.dim_x - being.U.shape[0] - 2, (self.dim_y - being.U.shape[1]) // 2)

    #def random(self):
    #    self.U[0] = np.random.choice([0, 1], (self.dim_x, self.dim_y))

    def step(self):
        self.run(1)

    def run(self, t):
        assert t >= 1

        self.T = np.arange(self.dim_t+1, self.dim_t+t+1)
        if self.dim_t == 0:
            self.U = np.append(self.U, self.U_0, axis=0)

        for t in self.T:
            self.U = np.append(self.U, np.zeros((1,self.dim_x, self.dim_y)), axis=0)

            for i in self.X:
                if i == 0 or i == self.dim_x - 1:
                    continue

                for j in self.Y:
                    if j == 0 or j == self.dim_y - 1:
                        continue

                    neig_sum = self.U[t - 1, i - 1, j + 1] + self.U[t - 1, i, j + 1] + \
                               self.U[t - 1, i + 1, j + 1] + self.U[t - 1, i - 1, j] + \
                               self.U[t - 1, i + 1, j] + self.U[t - 1, i - 1, j - 1] + \
                               self.U[t - 1, i, j - 1] + self.U[t - 1, i + 1, j - 1]
                    if self.U[t - 1, i, j] == 1:
                        self.U[t, i, j] = 1 if neig_sum in [2, 3] else 0
                    else:
                        self.U[t, i, j] = 1 if neig_sum == 3 else 0

            self.dim_t += 1

        return self.U
