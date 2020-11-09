"""
假设有一群羊在一个草场，羊在草场会吃草。
每天草场会生长草场最大总量的 20% (草场最大总量为固定值)，草场生长后不可超过其最大总量。
羊是否吃草完全随机，最小进食 0.1 单位，每天每只羊最多吃掉 0.5 个单位的草，没有吃够 0.5 单位的草就可能继续进食。
羊连续 3 天没吃就会饿死。
请模拟草场的草量与羊群数量 50 天的变化。
"""



import datetime
import random
from decimal import Decimal

EAT_UNIT = Decimal('0.1')
FULL_AMOUNT = Decimal('0.5')


class Sheep:

    def __init__(self, no: int):
        self.no = no
        self.eat_today = 0
        self.eat_nothing_count = 0
        self._is_alive = True

    def __eq__(self, other):
        return self.no == other.no

    def eat(self, unit=EAT_UNIT):
        assert self.is_alive
        self.eat_today = self.eat_today + unit

    @property
    def is_full(self, full_amount=FULL_AMOUNT):
        return self.eat_today >= full_amount

    def reset(self):
        assert self.is_alive
        if self.eat_today == 0:
            self.eat_nothing_count = self.eat_nothing_count + 1
        else:
            self.eat_nothing_count = 0
        self.eat_today = 0

    @property
    def is_alive(self):
        if self._is_alive:
            if self.eat_nothing_count >= 3:
                self._is_alive = False
                # print(f'{self} is dead!')
        return self._is_alive

    def __str__(self):
        return f'Sheep NO.{self.no}'


class Pasture:

    def __init__(self, max_grass: int, sheep_number: int):
        self.alive_unfull_sheep = [Sheep(i) for i in range(sheep_number)]
        self.alive_full_sheep = []
        self.dead_sheep = []
        self.grass_amount = max_grass
        self.MAX_GRASS = max_grass

    def grow(self, increase_rate=Decimal('0.2')):
        self.grass_amount += increase_rate * self.MAX_GRASS
        if self.grass_amount > self.MAX_GRASS:
            self.grass_amount = self.MAX_GRASS

    def start(self):
        self.grow()
        unfull_sheep = self.alive_unfull_sheep
        full_sheep = self.alive_full_sheep
        while (self.grass_amount > 0 and unfull_sheep):
            lucky = random.choice(unfull_sheep)
            lucky.eat()
            self.grass_amount = self.grass_amount - EAT_UNIT
            if lucky.is_full:
                unfull_sheep.remove(lucky)
                full_sheep.append(lucky)
        self.reset()

    def reset(self):
        alive_sheep = []
        for s in self.alive_unfull_sheep:
            s.reset()
            if s.is_alive:
                alive_sheep.append(s)
            else:
                self.dead_sheep.append(s)
        for s in self.alive_full_sheep:
            s.reset()
            alive_sheep.append(s)
        self.alive_unfull_sheep = alive_sheep
        self.alive_full_sheep = []


def simulate_with_class(max_grass: int, sheep_number: int):
    pasture = Pasture(max_grass, sheep_number)
    for i in range(50):
        pasture.start()
        print(f'day:{i+1};', f'grass: {pasture.grass_amount};', f'alive: {len(pasture.alive_unfull_sheep)};', f'dead: {len(pasture.dead_sheep)};')


def simulate_with_func(max_grass: int, sheep_number: int):
    grass_increase_rate =   Decimal('0.2')
    grass_amount = max_grass
    alive_sheep = [Sheep(i) for i in range(sheep_number)]

    for i in range(50):
        grass_amount += grass_increase_rate * max_grass
        if grass_amount > max_grass:
            grass_amount = max_grass
        # start eatting grass
        full_sheep = []
        unfull_sheep = alive_sheep
        while (grass_amount > 0 and unfull_sheep):
            lucky = random.choice(unfull_sheep)
            lucky.eat()
            grass_amount -= EAT_UNIT
            if lucky.is_full:
                unfull_sheep.remove(lucky)
                full_sheep.append(lucky)
        # Finished eating
        alive_sheep = []
        for s in unfull_sheep:
            s.reset()
            if s.is_alive:
                alive_sheep.append(s)
        for s in full_sheep:
            s.reset()
            alive_sheep.append(s)
        print(f'day:{i+1};', f'grass: {grass_amount};', f'alive: {len(alive_sheep)};', f'dead: {sheep_number-len(alive_sheep)};')


if __name__ == '__main__':
    params = input('Enter the amount of grass and sheep，separated by spaces\ninput: ')
    pl = params.split(' ')
    start = datetime.datetime.now()
    print(f'----start----: {start}')
    simulate_with_class(int(pl[0]), int(pl[-1]))
    simulate_with_func(int(pl[0]), int(pl[-1]))
    end = datetime.datetime.now()
    print(f'----end----: {end}')
    print(f'time consumed: {end-start}')

