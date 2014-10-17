#!/usr/bin/env python

# Imports #####################################################################
import unittest
import giantbomb
from giantbomb.tests.key import GIANT_BOMB_KEY
###############################################################################
class SanityTest(unittest.TestCase):
    game_title = '3-Demon'
    
    def test_basics(self):
        gb = giantbomb.Api(GIANT_BOMB_KEY)  
        print gb.search(self.game_title)


        
###############################################################################
if __name__ == "__main__":
    unittest.main()
