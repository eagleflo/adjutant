# adjutant

adjutant is a Python library for parsing and analyzing StarCraft II replay
files.

## Installation

A stable version of adjutant is available from PyPI and can be installed with
either `easy_install` or `pip`.

    easy_install adjutant
    pip install adjutant

adjutant can be installed manually with the included setup.py script.

    python setup.py install

Running any of these commands will install adjutant both as a library and a
stand-alone script that can be run from anywhere, provided that you have added
Python's bin directory to your PATH environment variable.

An alternative way to install adjutant is to clone this git repository. Note
that adjutant depends on [mpyq](http://github.com/arkx/mpyq/), a Python
library for reading MPQ files. You can either install it separately or just
clone it inside the adjutant repository.

    $ git clone git://github.com/arkx/adjutant.git
    # If you don't already have mpyq installed:
    $ cd adjutant
    $ git clone git://github.com/arkx/mpyq.git

## Usage

### As a library

    >>> from adjutant import SC2Replay
    >>> replay = SC2Replay('multi.SC2Replay')

You now have a SC2Replay object of the replay you opened. Some details of the
replay file were parsed.

    >>> replay.map
    'Toxic Slums'
    >>> replay.duration
    '26m 17s'
    >>> replay.version
    '1.0.2.16223'

Player details are stored inside dicts.

    >>> replay.players
    [{'color': 'Red', 'race': 'Protoss', 'name': 'narod', 'team': 1},
    {'color': 'Blue', 'race': 'Protoss', 'name': 'arkx', 'team': 1},
    {'color': 'Teal', 'race': 'Protoss', 'name': 'min', 'team': 1},
    {'color': 'Purple', 'race': 'Terran', 'name': 'liekki', 'team': 1},
    {'color': 'Yellow', 'race': 'Terran', 'name': 'Rev', 'team': 2},
    {'color': 'Orange', 'race': 'Zerg', 'name': 'Embegee', 'team': 2},
    {'color': 'Green', 'race': 'Protoss', 'name': 'Brutanic', 'team': 2},
    {'color': 'Light pink', 'race': 'Protoss', 'name': 'Blitzkrieg', 'team': 2}]

### From the command line

    usage: adjutant [-h] [-r] file

    adjutant parses and analyzes StarCraft II replays.

    positional arguments:
      file          path to the archive

    optional arguments:
      -h, --help    show this help message and exit
      -r, --rename  rename replay

Without any optional arguments, adjutant will display a summary of the
replay.

    adjutant multi.SC2Replay
    Map       Toxic Slums
    Duration  26m 17s
    Version   1.0.2.16223
    Team  Player       Race       Color
    -----------------------------------
    1     narod        Protoss    Red
    1     arkx         Protoss    Blue
    1     min          Protoss    Teal
    1     liekki       Terran     Purple
    2     Rev          Terran     Yellow
    2     Embegee      Zerg       Orange
    2     Brutanic     Protoss    Green
    2     Blitzkrieg   Protoss    Light pink

You can automatically rename a replay with `-r/--rename`.

    adjutant -r tlohasu.SC2Replay
    PvT.mouzHasu.vs.LiquidTLO.on.Metalopolis.2010-08-24-0644.SC2Replay

## Copyright

Copyright 2010, Aku Kotkavuo. See LICENSE for details.
