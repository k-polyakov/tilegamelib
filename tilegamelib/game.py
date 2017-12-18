
import os
import pygame
import time

from tilegamelib import EventGenerator
from tilegamelib import ExitListener
from tilegamelib import FigureMoveListener
from tilegamelib import TileFactory
from tilegamelib.config import config
from tilegamelib.draw_timer import draw_timer
from tilegamelib.move_group import MoveGroup

from .screen import Screen
from .frame import Frame


class Game:

    def __init__(self, config_filename=None, **kwargs):
        self.config = {}  # deprecated!
        if config_filename:
            self.parse_config(config_filename)
        self.screen = Screen()
        self.frame = Frame(self.screen, config.FRAME)
        self.tile_factory = TileFactory()
        self._exit = False

    def parse_config(self, config_filename):
        """
        Adds contents of config file to config dictionary.
        """
        # deprecated!
        path, fn = os.path.split(config_filename)
        self.path = path + os.sep
        before = set(dir())
        conf = open(config_filename).read()
        exec(conf)
        after = set(dir())
        for name in after - before:
            self.config[name] = eval(name)

    def event_loop(self, figure_moves=None, exit=True, draw_func=None):
        self.events = EventGenerator()
        if figure_moves:
            self.events.add_listener(FigureMoveListener(figure_moves))
        if exit:
            self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(draw_func, self.events):
            self.events.event_loop()

    def exit(self):
        self.events.exit_signalled()

    def wait_for_move(self, move=None, draw_func=None, delay=0.01):
        if type(move) is list:
            move = MoveGroup(move)
        while not move.finished:
            move.move()
            if draw_func:
                self.screen.clear()
                draw_func()
            move.draw()
            pygame.display.update()
            time.sleep(delay)
