# adjutant

adjutant is a Python library for parsing and analyzing StarCraft II replay
files.

## Installation

adjutant depends on [mpyq](http://github.com/arkx/mpyq/), a Python library for
reading MPQ files. If you're only interested in adjutant, an easy way to test
it is to first clone this adjutant repository and then clone mpyq inside it.

    $ git clone git://github.com/arkx/adjutant.git
    $ cd adjutant
    $ git clone git://github.com/arkx/mpyq.git

For now, adjutant is not installable as an egg. This will change in the
future.

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

    usage: adjutant.py [-h] [-r] file

    adjutant parses and analyzes StarCraft II replays.

    positional arguments:
      file          path to the archive

    optional arguments:
      -h, --help    show this help message and exit
      -r, --rename  rename replay

Without any optional arguments, adjutant will display a summary of the
replay.

    ./adjutant.py multi.SC2Replay
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

    ./adjutant.py -r tlohasu.SC2Replay
    PvT.mouzHasu.vs.LiquidTLO.on.Metalopolis.2010-08-24-0644.SC2Replay

## Copyright

Copyright 2010, Aku Kotkavuo. See LICENSE for details.
