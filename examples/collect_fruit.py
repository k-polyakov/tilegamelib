
import time

import pygame
from pygame import Rect

from tilegamelib import EventGenerator
from tilegamelib import ExitListener
from tilegamelib import FigureMoveListener
from tilegamelib import Frame
from tilegamelib import TiledMap
from tilegamelib import TileFactory
from tilegamelib import Vector
from tilegamelib.draw_timer import draw_timer
from tilegamelib.game import Game
from tilegamelib.move import wait_for_move
from tilegamelib.sprites import Sprite
from tilegamelib.config import config


FRUITMAP = """##########
#b.#...aa#
##.#.#####
#h.#.e#.c#
##.#.##.##
##a#.#f..#
#*..b..#g#
##########"""


class CollectFruit:

    def __init__(self, screen):
        self.screen = screen
        self.frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory()
        self.tm = TiledMap(self.frame, tile_factory)
        self.player = Sprite(self.frame, tile_factory.get('b.pac_right'),
                             Vector(4, 1), speed=4)
        self.tm.set_map(FRUITMAP)
        self.draw()
        self.events = None
        self.score = 0

    def draw(self):
        self.tm.draw()
        self.player.draw()
        pygame.display.update()

    def move(self, direction):
        nearpos = self.player.pos + direction
        near = self.tm.at(nearpos)
        if near == '#':
            return
        self.player.add_move(direction)
        wait_for_move(self.player, self.screen, self.draw, 0.01)
        self.check_player_square()

    def check_player_square(self):
        field = self.tm.at(self.player.pos)
        if field == '*':
            time.sleep(1)
            self.events.exit_signalled()
        elif field in 'abcdefgh':
            self.score += 100
            self.tm.set_tile(self.player.pos, '.')
            self.tm.cache_map()
            self.draw()

    def run(self):
        self.events = EventGenerator(game_delay=20)
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    game = Game(config.DATA_PATH + 'collect_fruit.conf', CollectFruit)
    game.run()
