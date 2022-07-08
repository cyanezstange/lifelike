from lifelike import Lifelike, Being

def viz():
    ###### VIZ ######
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.colors import ListedColormap
    #%matplotlib widget
    COLOR = 'black'

    matplotlib.rcParams['axes.linewidth'] = 4

    fig = plt.figure(figsize=(W/4,H/4))
    cm = ListedColormap(['white', COLOR])
    im = plt.imshow(U[0], cmap=cm)

    ax = plt.gca()
    ax.set_xticks(life.Y+0.5)
    ax.set_yticks(life.X+0.5)
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.grid(color='w', linestyle='-', linewidth=2)

    def animate(i):
        im.set_array(U[i])
        return [im]

    anim = FuncAnimation(fig, animate, frames=len(life.T), interval=100)

    anim.save('life.mp4')


if __name__ == '__main__':
    W = 8
    H = 8

    life = Lifelike(H, W)
    glider = Being('glider')
    life.add_being_middle(glider)

    life.run(20)

    U = life.U

    viz()
