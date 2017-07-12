
import time

import pygame
from pygame import Rect

from tilegamelib import EventGenerator
from tilegamelib import ExitListener
from tilegamelib import FigureMoveListener
from tilegamelib import Frame
from tilegamelib import Screen
from tilegamelib import TiledMap
from tilegamelib import TileFactory
from tilegamelib import Vector
from tilegamelib.draw_timer import draw_timer
from tilegamelib.map_move import MapMove
from tilegamelib.move import wait_for_move
from tilegamelib.move_group import MoveGroup
from tilegamelib.sprites import Sprite
from tilegamelib.config import config


BOXMAP = """##########
#..#...**#
#..#.##**#
#..#.##..#
##x....x.#
#.x.....x#
#........#
##########"""

config.RESOLUTION = Vector(450, 400)


class Boxes:

    def __init__(self):
        self.screen = Screen()
        self.frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory()
        self.tm = TiledMap(self.frame, tile_factory)
        self.player = Sprite(self.frame, tile_factory.get('b.tail'),
                             Vector(4, 1), speed=2)
        self.tm.set_map(BOXMAP)
        self.events = None

    def draw(self):
        self.tm.draw()
        self.player.draw()
        pygame.display.update()

    def move(self, direction):
        nearpos = self.player.pos + direction
        farpos = nearpos + direction
        near = self.tm.at(nearpos)
        far = self.tm.at(farpos)
        if near == '#':
            return
        if near in 'xX' and far in '#xX':
            return
        else:
            # move possible
            moves = MoveGroup()
            self.player.add_move(direction)
            moves.add(self.player)
            if near in 'xX':
                # crate moved
                floor = '.' if near == 'x' else '*'
                insert = 'X' if far == '*' else 'x'
                moves.add(MapMove(self.tm, nearpos, direction, 1,
                          floor_tile=floor, insert_tile=insert))

        wait_for_move(moves, self.screen, self.draw, 0.01)

        self.tm.cache_map()
        self.draw()
        self.check_complete()

    def check_complete(self):
        s = self.tm.get_map()
        if s.count('X') == 4:
            print("\nCongratulations!\n")
            time.sleep(2)
            self.events.exit_signalled()

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    boxes = Boxes()
    boxes.run()
