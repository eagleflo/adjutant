#!/usr/bin/env python
# coding: utf-8

"""
adjutant is a Python library for parsing StarCraft II replays.
"""

import argparse
import datetime
import os
import re
import StringIO
import struct
import sys
from collections import namedtuple, OrderedDict
from itertools import groupby

import mpyq


__author__ = "Aku Kotkavuo"
__version__ = "0.1"


COLORS = {
    'B4141E': 'Red',
    '0042FF': 'Blue',
    '1CA7EA': 'Teal',
    'EBE129': 'Yellow',
    '540081': 'Purple',
    'FE8A0E': 'Orange',
    '168000': 'Green',
    'CCA6FC': 'Light pink',
    '1F01C9': 'Violet',
    '525494': 'Light grey',
    '106246': 'Dark green',
    '4E2A04': 'Brown',
    '96FF91': 'Light green',
    '232323': 'Dark grey',
    'E55BB0': 'Pink'
}


def vlq2int(data):
    """Read one VLQ-encoded integer value from an input data stream."""
    # The VLQ is little-endian.
    byte = ord(data.read(1)) 
    value = byte & 0x7F
    shift = 1
    while byte & 0x80 != 0:
        byte = ord(data.read(1))
        value = ((byte & 0x7F) << shift * 7) | value
        shift += 1
    return value


def read_table(data, fields):
    """Read a table structure.

    These are used by Blizzard to collect pieces of data together. Each
    value is prefixed by two bytes, first denoting (doubled) index and the
    second denoting some sort of key -- so far it has always been '09'. The
    actual value follows as a Variable-Length Quantity, also known as uintvar.
    The actual value is also doubled.

    In some tables the keys might jump from 0A 09 to 04 09 for example.
    I have no idea why this happens, as the next logical key is 0C. Perhaps
    it's a table in a table? Some sort of headers might exist for these
    tables, I'd imagine at least denoting length. Further research required.
    """
    def read_field(field_name):
        data.read(2)
        table[field_name] = vlq2int(data) / 2
        # Discard unknown fields.
        if field_name == 'unknown':
            del table[field_name]

    table = {}
    for field in fields:
        read_field(field)
    return table


class SC2Replay(object):

    def __init__(self, archive):
        if isinstance(archive, mpyq.MPQArchive):
            self.archive = archive
        else:
            self.archive = mpyq.MPQArchive(archive)
        self._header = self._parse_header()
        self.version = self._header['version']
        self.duration = self.get_duration(self._header['duration'])
        self.players, self.map = self._parse_details()
        self.teams = dict((team, [p for p in players]) for (team, players) in
                          groupby(self.players, lambda x: x['team']))

    def _parse_header(self):
        """Parse the user data header portion of the replay."""
        header = OrderedDict()
        user_data_header = self.archive.header['user_data_header']['content']
        if re.search(r'StarCraft II replay', user_data_header):
            user_data_header = StringIO.StringIO(user_data_header)
            user_data_header.seek(30) # Just skip the beginning.
            header.update(read_table(user_data_header, ['release_flag',
                                                        'major_version',
                                                        'minor_version',
                                                        'maintenance_version',
                                                        'build_number',
                                                        'unknown',
                                                        'unknown',
                                                        'duration']))

            # Some post processing is required.
            header['version'] = '%s.%s.%s.%s' % (header['major_version'],
                                                 header['minor_version'],
                                                 header['maintenance_version'],
                                                 header['build_number'])
            if not header['release_flag']:
                header['version'] += ' (dev)'

            # Duration is actually stored as 1/16th of a seconds. Go figure.
            header['duration'] /= 16
        else:
            raise ValueError("The given file is not a StarCraft II replay.")
        return header

    def _parse_details(self):

        def read_player_struct():
            player = {}
            details.read(4)
            name_len = ord(details.read(1)) // 2
            player['name'] = details.read(name_len)
            details.read(5) # 02 05 08 00 09
            details.read(4) # 00/04 02 07 00
            details.read(3) # 00 00 00 // 00 53 32 (S2)
            read_table(details, ['unknown', 'unknown'])
            details.read(2) # 04 02
            race_len = ord(details.read(1)) // 2
            player['race'] = details.read(race_len)
            details.read(3) # 06 05 08
            values = {}
            values.update(read_table(details, ['alpha',
                                               'r',
                                               'g',
                                               'b',
                                               'unknown',
                                               'unknown',
                                               'unknown',
                                               'unknown',
                                               'team']))
            player['team'] = values['team']
            try:
                player['color'] = COLORS["%(r)02X%(g)02X%(b)02X" % values]
            except KeyError:
                player['color'] = "%(r)02X%(g)02X%(b)02X" % values
            return player

        details = StringIO.StringIO(self.archive.read_file('replay.details'))
        result = {}
        details.read(6) # 05 1C 00 04 01 00
        number_of_players = ord(details.read(1)) // 2
        result['players'] = []
        for player in range(number_of_players):
            result['players'].append(read_player_struct())
        details.read(2) # 02 02
        # Sort players by team by default.
        result['players'] = sorted(result['players'], key=lambda x: x['team'])
        map_name_len = ord(details.read(1)) // 2
        result['map'] = details.read(map_name_len)
        return result['players'], result['map']

    def get_duration(self, seconds):
        """Transform duration into a human-readable form."""
        duration = ""
        minutes, seconds = divmod(seconds, 60)
        if minutes >= 60:
            hours, minutes = divmod(minutes, 60)
            duration = "%sh " % hours
        duration += "%sm %ss" % (minutes, seconds)
        return duration

    def print_details(self):
        """Print a summary of the game details."""
        print 'Map      ', self.map
        print 'Duration ', self.duration
        print 'Version  ', self.version
        print 'Team  Player       Race       Color'
        print '-----------------------------------'
        for player in self.players:
            print '{team:<5} {name:12} {race:10} {color}'.format(**player)


def main(argv):
    description = "adjutant parses and analyzes StarCraft II replays."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", action="store", help="path to the archive")
    parser.add_argument("-r", "--rename", action="store_true", dest="rename",
                        help="rename replay")
    args = parser.parse_args()
    if args.file:
        replay = SC2Replay(args.file)
        if args.rename:
            races = 'v'.join(''.join(player['race'][0] for player in players)
                             for players in replay.teams.itervalues())
            names = '.vs.'.join('-'.join(player['name'] for player in players)
                             for players in replay.teams.itervalues())
            map_name = replay.map.replace(' ', '_')
            time = datetime.datetime.fromtimestamp(os.path.getctime(args.file))
            time = time.strftime('%Y-%m-%d-%H%M')
            replay_name = "%s.%s.on.%s.%s.SC2Replay" % (races,
                                                        names,
                                                        map_name,
                                                        time)
            print replay_name
            os.rename(args.file, replay_name)
        else:
            replay.print_details()


if __name__ == '__main__':
    main(sys.argv)
