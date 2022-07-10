from lifelike import Lifelike

life = Lifelike(40, 40)
life.add_pattern('lobster', 'bottom_right', offset=(-1,-1))
life.run(250)

life.to_file('lobster.gif')
