from lifelike import Lifelike, Being

url_glider               = 'https://www.conwaylife.com/patterns/glider.rle'
url_gosperglidergun      = 'https://www.conwaylife.com/patterns/gosperglidergun.rle'
url_transqueenbeeshuttle = 'https://www.conwaylife.com/patterns/transqueenbeeshuttle.rle'
url_lobster              = 'https://www.conwaylife.com/patterns/lobster.rle'
url_232p7h3v0            = 'https://www.conwaylife.com/patterns/232p7h3v0.rle'
url_p27glidergun         = 'https://www.conwaylife.com/patterns/period27glidergun.rle'

W = 80
H = 80
life = Lifelike(H, W, 200)

asdf    = Being(url_232p7h3v0)
lobster = Being(url_lobster)
glider  = Being(url_glider)
queen   = Being(url_transqueenbeeshuttle)
gosper  = Being(url_gosperglidergun)
p27     = Being(url_p27glidergun)

life.add_being_middle(p27)
U = life.run()  # <--- t

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
