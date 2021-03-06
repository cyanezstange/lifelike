import numpy as np
from lifelike import Pattern

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
            U_temp = self.U_0[0]
        else:
            U_temp = self.U[-1]

        out = ''
        for row in U_temp:
            for elem in row:
                out += '@' if elem==1 else ' '
            out += '\n'

        return out

    def add_pattern(self, pattern, pos, offset=(0,0)):
        # Chack type: pattern.
        if isinstance(pattern, Pattern):
            pass
        elif isinstance(pattern, str):
            pattern = Pattern(pattern)
        else:
            #TODO Raise exception.
            print('Error: pattern not instance of Pattern nor str.')

        # Chack type: pos.
        # Definition of x and y.
        positions = {
            'top_left'     : (1, 1),
            'middle'       : ((self.dim_x - pattern.U.shape[0]) // 2,
                              (self.dim_y - pattern.U.shape[1]) // 2),
            'bottom_right' : ((self.dim_x - pattern.U.shape[0]),
                              (self.dim_y - pattern.U.shape[1])),
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
            self.rule = pattern.rule

        if self.rule == pattern.rule:
            if self.dim_t == 0:
                self.U_0[0][x:x + pattern.U.shape[0], y:y + pattern.U.shape[1]] = pattern.U
            else:
                self.U[-1][x:x + pattern.U.shape[0], y:y + pattern.U.shape[1]] = pattern.U
        else:
            #TODO Raise exception
            print('Error: Rule mismatch.')

    #def random(self):
    #    self.U[0] = np.random.choice([0, 1], (self.dim_x, self.dim_y))

    def to_file(self, filename='life.mp4'):
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

        anim = FuncAnimation(fig, animate, frames=len(self.U), interval=100)

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
