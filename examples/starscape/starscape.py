
import os
import time

import pygame
from pygame import image
from pygame import Rect

from create_stars import STAR_PATH
from tilegamelib import Frame
from tilegamelib import Screen
from tilegamelib import Vector
from tilegamelib.config import config


class StarScape:
    """Draws a parallax-scrolling background"""
    def __init__(self, frame, path=STAR_PATH):
        self.frame = frame
        self.stars = [
            image.load(os.path.join(path, 'stars1.png')).convert_alpha(),
            image.load(os.path.join(path, 'stars2.png')).convert_alpha(),
            image.load(os.path.join(path, 'stars3.png')).convert_alpha()
        ]
        self.offsets = [0, 0, 0]
        self.increments = [4, 2, 1]

    def draw(self):
        rsrc = Rect(0, 0, 800, 600)
        for i in range(3):
            rdest = Rect(self.offsets[i] - 800, 0, 800, 600)
            self.frame.blit(self.stars[i], rsrc, rdest)
            rdest = Rect(self.offsets[i], 0, 800, 600)
            self.frame.blit(self.stars[i], rsrc, rdest)

    def scroll(self):
        for i in range(3):
            self.offsets[i] += self.increments[i]
            if self.offsets[i] >= 800:
                self.offsets[i] = 0


if __name__ == '__main__':
    screen = Screen()
    frame = Frame(screen, Rect(0, 0, 800, 600))
    starscape = StarScape(frame)

    while True:
        screen.clear()
        starscape.draw()
        starscape.scroll()
        pygame.display.update()
        time.sleep(0.01)
