
import pygame

from tilegamelib.basic_boxes import ImageBox, TextBox
from tilegamelib.config import config
from tilegamelib.event_listener import AnyKeyListener
from tilegamelib.events import EventGenerator


class GamePausedBox:
    """Displays a pause box."""

    def __init__(self, frame, image=None, text=config.PAUSE_TEXT, egen=None):
        """Initializes the Pause Box."""
        self.image = ImageBox(frame, image)
        self.text = TextBox(frame, text)
        if egen is None:
            egen = EventGenerator()
        self.egen = egen
        self.elis = AnyKeyListener(self.pause_ended)
        self.egen.add_listener(self.elis)

    def pause_ended(self):
        """Pause ended."""
        self.egen.remove_listener(self.elis)

    def draw(self):
        """Draws the Pause Box."""
        self.image.draw()
        self.text.draw()

    def activate(self):
        self.draw()
        pygame.display.update()
        self.egen.event_loop()


'''
def pause_game(paused_state):
    self.paused_state = paused_state
    frame = Frame(self.screen, self.data['PAUSE_BOX_RECT'])
    pause = GamePausedBox(frame, self.data['PAUSE_IMAGE'],
        'Game paused - press any key', self.event_generator)
    pause.activate()
'''
