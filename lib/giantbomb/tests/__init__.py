#!/usr/bin/env python

# Imports #####################################################################
import unittest
import giantbomb
try:
    from giantbomb.tests.key import GIANT_BOMB_KEY
except ImportError:
    import os
    GIANT_BOMB_KEY = os.environ['GIANT_BOMB_KEY']


###############################################################################
class SanityTest(unittest.TestCase):
    game_title = 'uscf'
    plat_id = 548  # atari
    plat_name = 'atari'

    def setUp(self):
        self.gb = giantbomb.Api(GIANT_BOMB_KEY)

    def test_get_franchise(self):
        results = self.gb.get_franchise(42)
        self.assertTrue(isinstance(results, giantbomb.Franchise))

    def test_get_franchises(self):
        results = self.gb.get_franchises(offset=1)[0]
        self.assertTrue(isinstance(results, giantbomb.Franchise))

        results = self.gb.get_franchises(limit=2)[0]
        self.assertTrue(isinstance(results, giantbomb.Franchise))

        results = self.gb.get_franchises(offset=1, limit=10)
        self.assertTrue(isinstance(results[0], giantbomb.Franchise))
        self.assertEqual(len(results), 10)

    def test_get_game(self):
        game1 = self.gb.search(self.game_title)[0]

        game2 = self.gb.get_game(game1.id)
        self.assertTrue(isinstance(game2, giantbomb.Game))

        game3 = self.gb.get_game(game1)
        self.assertTrue(isinstance(game3, giantbomb.Game))

        self.assertEqual(game1.name, game2.name)
        self.assertEqual(game2.name, game3.name)

    def test_get_games(self):
        results = self.gb.get_games(plat=self.plat_id)[0]
        self.assertTrue(isinstance(results, giantbomb.SearchResult))

        results = self.gb.get_games(plat=self.plat_id, offset=10)[0]
        self.assertTrue(isinstance(results, giantbomb.SearchResult))

        results = self.gb.get_games(offset=10)[0]
        self.assertTrue(isinstance(results, giantbomb.SearchResult))

        results = self.gb.get_games(plat=self.plat_id, offset=10,
                                    gbfilter={'name': self.game_title})[0]
        self.assertTrue(isinstance(results, giantbomb.SearchResult))

        results = self.gb.get_games(plat=self.plat_id,
                                    gbfilter={'name': self.game_title})[0]
        self.assertTrue(isinstance(results, giantbomb.SearchResult))

        results = self.gb.get_games(plat=self.plat_id, limit=10,
                                    gbfilter={'name': self.game_title})
        self.assertTrue(isinstance(results[0], giantbomb.SearchResult))
        self.assertEqual(len(results), 10)

    def test_get_platform(self):
        results = self.gb.get_platform(42)
        self.assertTrue(isinstance(results, giantbomb.Platform))

    def test_get_platforms(self):
        results = self.gb.get_platforms(offset=42)[0]
        self.assertTrue(isinstance(results, giantbomb.Platform))

        results = self.gb.get_platforms(offset=1,
                                        gbfilter={'name': self.plat_name})[0]
        self.assertTrue(isinstance(results, giantbomb.Platform))

        results = self.gb.get_platforms(offset=1, limit=10)
        self.assertTrue(isinstance(results[0], giantbomb.Platform))
        self.assertEqual(len(results), 10)

    def test_search(self):
        results = self.gb.search(self.game_title)[0]
        self.assertTrue(isinstance(results, giantbomb.SearchResult))

    def test_get_video(self):
        results = self.gb.get_video(42)
        self.assertTrue(isinstance(results, giantbomb.Video))


###############################################################################
if __name__ == "__main__":
    unittest.main()
