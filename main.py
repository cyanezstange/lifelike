from lifelike import Lifelike

life = Lifelike(40, 40)
life.add_being('lobster', 'bottom_right', offset=(-1,-1))
for _ in range(20):
    life.add_being('glider', (1,1))
    life.run(20)
life.viz()
