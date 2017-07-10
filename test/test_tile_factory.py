
import pygame
from pygame import Rect
import pytest

from data import TILE_SPECS
from tilegamelib.tile_factory import NoTileError
from tilegamelib.tile_factory import TileFactory
from tilegamelib.tiles import Tile
from util import showdoc
from util import TEST_GAME_CONTEXT


class TestTileFactory:

    def test_get_tiles(self):
        """Factory produces tiles."""
        tfac = TileFactory(TILE_SPECS)
        wall = tfac.get('b.wall')
        assert isinstance(wall, Tile)

    def test_tile_synonyms(self):
        """Tiles can be addressed by abbreviations"""
        tfac = TileFactory(TILE_SPECS)
        assert isinstance(tfac.get('.'), Tile)
        assert isinstance(tfac.get('#'), Tile)
        assert isinstance(tfac.get('*'), Tile)
        assert isinstance(tfac.get('x'), Tile)

    def test_notile_found(self):
        """Unknown tile raises exception"""
        tfac = TileFactory(TILE_SPECS)
        with pytest.raises(NoTileError):
            tfac.get('unkown_tile')

    @pytest.fixture
    def tile_factory(self):
        """Loads the default factory"""
        return TileFactory(TILE_SPECS)

    def test_tile_identity(self, tile_factory):
        """Abbreviations for tiles match full name"""
        assert tile_factory.get('b.wall') == tile_factory.get('#')
        assert tile_factory.get('b.wall') != tile_factory.get('.')

    def test_add_synonym(self, tile_factory):
        """Synonyms can be added"""
        tile_factory.add_tile_synonyms({'w': 'b.wall'})
        assert tile_factory.get('w')

    def test_w_not_used(self, tile_factory):
        """adding synonym is not global"""
        with pytest.raises(NoTileError):
            tile_factory.get('w')

    @showdoc
    def test_display_tiles(self):
        """Display three tiles from factory"""
        screen = TEST_GAME_CONTEXT.screen
        tfac = TileFactory(TILE_SPECS)
        tfac.get('b.wall').draw(screen, Rect(32, 32, 32, 32))
        tfac.get('x').draw(screen, Rect(32, 64, 32, 32))
        tfac.get('*').draw(screen, Rect(64, 32, 32, 32))
        pygame.display.update()
