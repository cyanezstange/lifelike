from lifelike import Lifelike

if __name__ == '__main__':
    life = Lifelike(8, 8)
    life.add_being('glider', 'top_left')
    life.run(20)
    life.viz()
