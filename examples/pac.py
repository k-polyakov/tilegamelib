
import random
import time
import numpy as np

import pygame
from pygame import Rect

from tilegamelib import TiledMap
from tilegamelib.bar_display import BarDisplay
from tilegamelib.basic_boxes import DictBox
from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP

ONE_PLAYER_START_DELAY = 3000


LEVEL = """####################
#.****************e#
#*#*#######*####*#*#
#*#*******#c*****#*#
#*#*#####**c####*#*#
#*********###******#
#*##*####f****#*##*#
#*##*#***f#####*##*#
#******#***********#
#*#*####*##**##*##*#
#e****************e#
####################"""

config.RESOLUTION = (850, 450)

config.HIGHSCORES = True
config.HIGHSCORE_FILE = config.DATA_PATH + 'pac_scores.txt'

config.BOX_IMAGE = config.DATA_PATH + 'frame_box.png'
config.KEY_REPEAT = {}
config.GAME_KEY_REPEAT = { 273:1, 274:1, 275:1, 276:1}

PAC_START = np.array([1, 1])
GHOST_POSITIONS = [(18, 1),
                   (18, 10),
                   (1, 10)]

PAC_TILES = {
    str(UP): 'b.pac_up',
    str(DOWN): 'b.pac_down',
    str(LEFT): 'b.pac_left',
    str(RIGHT): 'b.pac_right'
}

GHOST_TILE = 'b.ghost'


class PacLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))
        self.dots_left = data.count("*")

    def at(self, pos):
        return self.tmap.at(pos)

    def remove_dot(self, pos):
        tile = self.at(pos)
        if tile != '.':
            self.tmap.set_tile(pos, '.')
            if tile == '*':
                self.dots_left -= 1

    def draw(self):
        self.tmap.draw()


class Ghost:

    def __init__(self, game, pos, level):
        self.sprite = Sprite(game, GHOST_TILE, pos, speed=2)
        self.level = level
        self.direction = None
        self.set_random_direction()

    def get_possible_moves(self):
        result = []
        directions = [LEFT, RIGHT, UP, DOWN]
        for vector in directions:
            if not all(vector * -1 == self.direction):
                newpos = self.sprite.pos + vector
                tile = self.level.at(newpos)
                if tile != '#':
                    result.append(vector)
        if not result:
            result = [self.direction * (-1)]
        return result

    def set_random_direction(self):
        moves = self.get_possible_moves()
        self.direction = random.choice(moves)

    def move(self):
        if self.sprite.finished:
            self.set_random_direction()
            self.sprite.add_move(self.direction)
        else:
            self.sprite.move()

    def update(self):
        self.move()

    def draw(self):
        self.sprite.draw()


class Pac:

    def __init__(self, game, pos, level):
        self.game = game
        self.level = level
        self.sprite = Sprite(game, 'b.pac_right', pos, speed=4)
        self.direction = RIGHT
        self.eaten = None
        self.score = 0
        self.buffered_move = None

    def set_direction(self, direction):
        self.sprite.tile = self.game.get_tile(PAC_TILES[str(direction)])
        self.direction = direction
        self.move()

    def move(self, direction=None):
        if direction is None:
            direction = self.direction
        if not self.sprite.finished:
            self.buffered_move = direction
            return
        newpos = self.sprite.pos + direction
        tile = self.level.at(newpos)
        if tile != '#':
            self.sprite.add_move(direction, when_finished=self.try_eating)

    def try_eating(self):
        tile = self.level.at(self.sprite.pos)
        if tile != '.':
            self.level.remove_dot(self.sprite.pos)
            if tile == '*':
                self.score += 100
            else:
                self.score += 1000
            self.eaten = tile

    def update(self):
        """Try eating dots and fruit"""
        if self.sprite.finished and not self.buffered_move is None:
            self.move(self.buffered_move)
            self.buffered_move = None
        if not self.sprite.finished:
            self.sprite.move()
        else:
            self.move()

    def draw(self):
        self.sprite.draw()

    def collision(self, sprites):
        for sprite in sprites:
            if all(self.sprite.pos == sprite.sprite.pos):
                return True

    def die(self):
        self.buffered_move = None
        self.sprite.path = []


class PacGame:

    def __init__(self):
        self.game = Game()

        self.level = None
        self.pac = None
        self.ghosts = []
        self.status_box = None

        self.create_level()
        self.create_pac()
        self.create_ghosts()
        self.create_status_box()
        frame = Frame(self.game.screen, Rect(660, 220, 200, 200))
        self.lives = BarDisplay(frame, self.game, 3, 'p')

        self.collided = False
        self.mode = None
        self.update_mode = self.update_ingame

    def create_level(self):
        tmap = TiledMap(self.game)
        self.level = PacLevel(LEVEL, tmap)

    def create_pac(self):
        self.pac = Pac(self.game, PAC_START, self.level)
        self.pac.set_direction(RIGHT)

    def create_ghosts(self):
        self.ghosts = []
        for pos in GHOST_POSITIONS:
            self.ghosts.append(Ghost(self.game, pos, self.level))

    def reset_level(self):
        self.pac.sprite.pos = np.array(PAC_START)  # TODO: create setter in Sprite
        self.create_ghosts()

    def create_status_box(self):
        frame = Frame(self.game.screen, Rect(660, 20, 200, 200))
        data = {
            'score': 0,
            'level': 1,
        }
        self.status_box = DictBox(frame, data)

    def check_collision(self):
        if self.pac.collision(self.ghosts):
            self.update_mode = self.update_die
            self.pac.die()
            self.collided = True

    def update_die(self):
        """finish movements"""
        if self.pac.sprite.finished:
            time.sleep(1)
            self.lives.decrease()
            if self.lives.value == 0:
                self.game.exit()
            else:
                self.reset_level()
                self.game.events.empty_event_queue()
                self.update_mode = self.update_ingame

    def update_level_complete(self):
        """finish movement"""
        if self.pac.sprite.finished:
            time.sleep(1)
            self.game.exit()

    def update_ingame(self):
        self.check_collision()
        if self.pac.eaten:
            self.status_box.data['score'] = self.pac.score
            self.pac.eaten = None
            self.score = self.pac.score
        if self.level.dots_left == 0:
            self.update_mode = self.update_level_complete

    def draw(self):
        self.update_mode()
        self.level.draw()
        self.pac.update()
        self.pac.draw()
        for g in self.ghosts:
            g.update()
            g.draw()
        self.status_box.draw()
        self.check_collision()

    def run(self):
        self.mode = self.update_ingame
        self.game.event_loop(figure_moves=self.pac.set_direction,
            draw_func=self.draw)


if __name__ == '__main__':
    config.FRAME = Rect(10, 10, 640, 512)
    pac = PacGame()
    pac.run()
    pygame.quit()
