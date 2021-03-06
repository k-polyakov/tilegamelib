#! /usr/bin/python

import random
import time

import pygame
from pygame import Rect

from tilegamelib import Frame
from tilegamelib import TiledMap
from tilegamelib.basic_boxes import DictBox
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP
from tilegamelib.config import config

MOVE_DELAY = 15


LEVEL = """####################
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
####################"""

MOVE_OK = 1
MOVE_CRASH = 2
HEAD_SPEED = 4

HEAD_TILES = {
    str(UP): 'b.pac_up',
    str(DOWN): 'b.pac_down',
    str(LEFT): 'b.pac_left',
    str(RIGHT): 'b.pac_right'
}

EASY = False

config.RESOLUTION = (800, 550)


class SnakeLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))

    def place_fruit(self, pos, fruit):
        self.tmap.set_tile(pos, fruit)

    def remove_fruit(self, pos):
        tile = self.tmap.at(pos)
        if tile != '.':
            self.tmap.set_tile(pos, '.')

    def place_random_fruit(self):
        x = random.randint(1, self.tmap.size.x - 2)
        y = random.randint(1, self.tmap.size.y - 2)
        fruit = random.randint(0, 5)
        self.place_fruit((x, y), 'abcdef'[fruit])

    def draw(self):
        self.tmap.draw()


class SnakeSprite:

    def __init__(self, game, pos, level):
        self.game = game
        self.level = level
        self.head = None
        self.tail = []
        self.tail_waiting = []
        self.head = Sprite(self.game, 'b.pac_right', pos, HEAD_SPEED)
        self.direction = RIGHT
        self.past_directions = []
        self.crashed = False
        self.eaten = ''

    @property
    def length(self):
        return 1 + len(self.tail) + len(self.tail_waiting)

    @property
    def sprites(self):
        return [self.head] + self.tail

    def is_moving(self):
        if not self.head.finished:
            return True

    def set_direction(self, direction):
        # prevent reverse move
        if len(self.tail) > 0 and direction == self.past_directions[0] * -1:
            return
        self.direction = direction
        headtile = HEAD_TILES[str(direction)]
        self.head.tile = self.game.get_tile(headtile)
        if EASY:
            self.move_forward()

    def draw(self):
        for s in self.sprites:
            s.draw()

    def move(self):
        if self.is_moving():
            for s in self.sprites:
                s.move()

    @property
    def positions(self):
        return [self.head.pos] + [seg.pos for seg in self.tail]

    def grow(self):
        self.tail_waiting.append(Sprite(self.game, 'b.tail', self.positions[-1], HEAD_SPEED))
        if not self.past_directions:
            self.past_directions.append(self.direction)
        else:
            self.past_directions.append(self.past_directions[-1])

    def move_forward(self):
        newpos = self.head.pos + self.direction
        tile = self.level.tmap.at(newpos)
        if newpos in self.positions or tile == '#':
            self.crashed = True
        else:
            self.head.add_move(self.direction)
            if self.tail_waiting:
                self.tail.append(self.tail_waiting.pop())
            for sprite, direction in zip(self.tail, self.past_directions):
                sprite.add_move(direction)
            if tile != '.':
                self.grow()
                self.eaten = tile
            if len(self.tail) > 0:
                self.past_directions = [self.direction] + self.past_directions[:-1]


class SnakeGame:

    def __init__(self):
        self.game = Game()

        self.level = None
        self.snake = None
        self.status_box = None
        self.events = None
        self.score = 0

        self.create_level()
        self.create_snake()
        self.create_status_box()

        self.update_mode = self.update_ingame
        self.move_delay = MOVE_DELAY
        self.delay = MOVE_DELAY

    def create_snake(self):
        start_pos = (5, 5)
        self.snake = SnakeSprite(self.game, start_pos, self.level)
        self.snake.set_direction(RIGHT)

    def create_level(self):
        tmap = TiledMap(self.game)
        self.level = SnakeLevel(LEVEL, tmap)
        self.level.place_random_fruit()

    def create_status_box(self):
        frame = Frame(self.game.screen, Rect(660, 20, 200, 200))
        self.status_box = DictBox(frame, {'score': 0})

    def update_finish_moves(self):
        """finish movements before Game Over"""
        if not self.snake.is_moving():
            pygame.display.update()
            time.sleep(1)
            self.game.exit()

    def update_ingame(self):
        self.delay -= 1
        if self.delay <= 0:
            self.delay = self.move_delay
            if not EASY:
                self.snake.move_forward()
        if self.snake.eaten and not self.snake.is_moving():
            self.level.remove_fruit(self.snake.head.pos)
            self.level.place_random_fruit()
            self.status_box.data['score'] += 100
            self.snake.eaten = None
        if self.snake.crashed:
            self.update_mode = self.update_finish_moves
            self.score = self.status_box.data['score']

    def update(self):
        self.update_mode()
        self.snake.move()

    def draw(self):
        self.update()
        self.level.draw()
        self.snake.draw()
        self.status_box.draw()

    def run(self):
        self.game.event_loop(figure_moves=self.snake.set_direction, draw_func=self.draw)


if __name__ == '__main__':
    config.FRAME = Rect(10, 10, 640, 512)
    snake = SnakeGame()
    snake.run()
    pygame.quit()
