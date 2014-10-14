|travis ci build state|

|rtd state|

Introduction
------------

## Python wrapper for Giantbomb API!
**Get your API Key at http://api.giantbomb.com**

Basic usage:  

    import giantbomb  
    gb = giantbomb.Api('YOUR_KEY')
    
**Current Methods:**  

 * search(str, offset)
 * getGame(game_id)
 * getGames(platform_id, offset)
 * getVideo(video_id)
 * getPlatform(platform_id)
 * getPlatforms(offset)
 * getFranchise(franchise_id)
 * getFranchises(offset)
 
*Everything returns an object:*  

Documentation
-------------

Documentation is hosted on [libdlm.readthedocs.org](http://GiantBomb.readthedocs.org/en/latest/)

Install
-------

Download the tarball and install with `pip install <package>`.

Usage
-----

See the unit tests for more in-depth examples. Here are the basics:

    import giantbomb  
    gb = giantbomb.Api('YOUR_KEY')  
    
    games = gb.getGames(94, 12300) // 94 = PC
    print games
    
    >>> [<29220: Zero Gear>, <29234: Pro Cycling Manager: Season 2010>,
         <29238: Allods Online>, <29240: Hammerfight>, <29247: Sacraboar>,
         <29249: POWDER>, <29257: Grand Fantasia>, ...]
    
    ------------------------------------------------------------------------------
    
    results = gb.search('call of duty')
    print results
    
    >>> [<26423: Call of Duty: Black Ops>, <2133: Call of Duty 4: Modern Warfare>,
         <20777: Call of Duty: World at War>, ...]
    
    game = gb.getGame(26423) // or gb.getGame(results[0])
    for p in game.platforms:
        print p.name
        
    >>> PlayStation 3
        Wii
        Nintendo DS
        PlayStation Network (PS3)
        Xbox 360
        PC

.. |travis ci build state| image:: https://travis-ci.org/JasonAUnrein/GiantBomb.svg?branch=master
   :target: https://travis-ci.org/JasonAUnrein/GiantBomb
.. |rtd state| image:: https://readthedocs.org/projects/GiantBomb/badge/?version=latest
   :target: https://readthedocs.org/projects/GiantBomb/?badge=latest