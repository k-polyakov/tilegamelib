
import time
from unittest import main
from unittest import TestCase

import pygame
from pygame import Rect

from data import SAMPLE_MAP_FILE
from tilegamelib.frame import Frame
from tilegamelib.move import Move
from tilegamelib.tiled_map import TiledMap
from tilegamelib.vector import DOWN
from tilegamelib.vector import DOWNLEFT
from tilegamelib.vector import LEFT
from tilegamelib.vector import UP
from tilegamelib.vector import UPLEFT
from tilegamelib.vector import UPRIGHT
from tilegamelib.vector import Vector
from util import DELAY
from util import SHORT_DELAY
from util import showdoc
from util import TEST_GAME_CONTEXT


class TiledMapTests(TestCase):

    def setUp(self):
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(90, 50, 128, 128))
        self.tm = TiledMap(frame, TEST_GAME_CONTEXT.tile_factory)

    def test_fill_map(self):
        self.tm.set_map(TEST_MAP)

    def test_caching(self):
        bigmap = ["." * 50 for i in range(50)]
        self.tm.set_map('\n'.join(bigmap))
        for i in range(10):
            self.tm.cache_map()

    def test_win_size(self):
        self.tm.set_map(TEST_MAP)
        self.assertEqual(self.tm.win_size.x, 4)
        self.assertEqual(self.tm.win_size.y, 4)

    def test_is_visible(self):
        self.tm.set_map(TEST_MAP)
        self.assertTrue(self.tm.is_visible(Vector(0, 0)))
        self.assertTrue(self.tm.is_visible(Vector(1, 1)))
        self.assertFalse(self.tm.is_visible(Vector(5, 1)))
        self.assertFalse(self.tm.is_visible(Vector(1, 5)))
        self.assertFalse(self.tm.is_visible(Vector(-5, -1)))

    def test_check_position(self):
        self.tm.set_map(TEST_MAP)
        self.assertFalse(self.tm.check_position(Vector(-1, -1)))
        self.assertFalse(self.tm.check_position(Vector(5, 1)))
        self.assertFalse(self.tm.check_position(Vector(1, 5)))
        self.assertTrue(self.tm.check_position(Vector(0, 0)))
        self.assertTrue(self.tm.check_position(Vector(1, 1)))
        self.assertTrue(self.tm.check_position(Vector(4, 4)))

    def test_check_move(self):
        self.tm.set_map(TEST_MAP)
        self.assertFalse(self.tm.check_move(Vector(-1, -1)))
        self.assertTrue(self.tm.check_move(Vector(1, 1)))
        self.tm.zoom_to(Vector(1, 1))
        self.assertFalse(self.tm.check_move(Vector(1, 1)))
        self.assertTrue(self.tm.check_move(Vector(-1, -1)))

    def test_zoom_to(self):
        self.tm.set_map(TEST_MAP)
        self.tm.zoom_to(Vector(1, 1))
        self.assertEqual(self.tm.map_pos.x, 1)
        self.assertEqual(self.tm.map_pos.y, 1)

    # def test_load_map(self):
    #     self.tm.load_map(SAMPLE_MAP_FILE)
    #     self.assertEqual(len(self.tm.map), 10)
    #     self.assertEqual(len(self.tm.map[0]), 10)

    @showdoc
    def test_draw(self):
        """Draws two 5x5 locations of a map with boxes."""
        self.tm.set_map(open(SAMPLE_MAP_FILE).read())
        self.tm.draw()
        pygame.display.update()
        time.sleep(DELAY)
        self.tm.zoom_to(Vector(4, 4))
        self.tm.draw()
        pygame.display.update()


# class MoveableTiledMapTests(TestCase):

#     def setUp(self):
#         frame = Frame(TEST_GAME_CONTEXT.screen, Rect(90, 50, 160, 160))
#         self.tm = TiledMap(frame, TEST_GAME_CONTEXT.tile_factory)

#     def move_tiles(self):
#         while self.tm.is_map_moving():
#             self.tm.update()
#             self.tm.draw()
#             pygame.display.update()
#             time.sleep(SHORT_DELAY)

#     @showdoc
#     def test_move_map_tile(self):
#         """Moves two tiles right and up, then moves one tile back."""
#         self.tm.set_map(TEST_MAP)
#         self.tm.move_tile(Move(Vector(3,1), DOWNLEFT, 3, 2))
#         self.tm.move_tile(Move(Vector(1,2), UP, 1, 1))
#         self.move_tiles()
#         # move one piece back
#         self.tm.move_tile(Move(Vector(0,0), DOWN, 1, 4))
#         self.tm.move_tile(Move(Vector(0,4), UPRIGHT, 3, 2))
#         self.move_tiles()

#     @showdoc
#     def test_queued_moves(self):
#         """Two 2+1 moves across the map shown."""
#         self.tm.set_map(TEST_MAP)
#         self.tm.add_queued_moveset(
#                 [Move(Vector(0,0), DOWN, 3, 2),
#                  Move(Vector(2,1), UPLEFT, 1, 4)])
#         self.tm.add_queued_moveset([Move(Vector(3,3), LEFT, 2, 1)])
#         self.move_tiles()



TEST_MAP = """#...#
.aaa.
.p#b.
.aaa.
#...#"""

TEST_LINES = [".....",".....",".....",".....","....."]

if __name__ == "__main__":
    main()
