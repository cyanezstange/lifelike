import numpy as np
from lifelike import Being

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap


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

    def add_being(self, being, pos, offset=(0,0)):
        # Chack type: being.
        if isinstance(being, Being):
            pass
        elif isinstance(being, str):
            being = Being(being)
        else:
            #TODO Raise exception.
            print('Error: being not instance of Being nor str.')

        # Chack type: pos.
        # Definition of x and y.
        positions = {
            'middle'   : ((self.dim_x - being.U.shape[0]) // 2,
                          (self.dim_y - being.U.shape[1]) // 2),
            'top_left' : (1, 1),
        }
        if isinstance(pos, tuple) and len(pos) == 2:
            x, y = pos
        elif pos in positions:
            x, y = positions[pos]
        else:
            #TODO Raise exception
            print('Error: Bad position.')

        # Check type offset.
        if isinstance(offset, tuple) and len(offset) == 2:
            x += offset[0]
            y += offset[1]
        else:
            #TODO Raise exception
            print('Error: Bad offset.')

        if self.rule == None:
            self.rule = being.rule

        if self.rule == being.rule:
            self.U_0[0][x:x + being.U.shape[0], y:y + being.U.shape[1]] = being.U
        else:
            #TODO Raise exception
            print('Error: Rule mismatch.')

    #def random(self):
    #    self.U[0] = np.random.choice([0, 1], (self.dim_x, self.dim_y))

    def viz(self, filename='life.mp4'):
        COLOR = 'black'

        matplotlib.rcParams['axes.linewidth'] = 4

        fig = plt.figure(figsize=(self.dim_x/4, self.dim_y/4))
        cm = ListedColormap(['white', COLOR])
        im = plt.imshow(self.U[0], cmap=cm)

        ax = plt.gca()
        ax.set_xticks(self.Y+0.5)
        ax.set_yticks(self.X+0.5)
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        plt.grid(color='w', linestyle='-', linewidth=2)

        def animate(i):
            im.set_array(self.U[i])
            return [im]

        anim = FuncAnimation(fig, animate, frames=len(self.T), interval=100)

        anim.save(filename)

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
