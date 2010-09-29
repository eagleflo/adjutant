#!/usr/bin/env python
# coding: utf-8

import os
import unittest
from adjutant import SC2Replay

TEST_DIR = os.path.realpath(os.path.dirname(__file__)) + '/'

class TestSC2Replay(unittest.TestCase):

    def setUp(self):
        self.replay = SC2Replay(TEST_DIR + 'test.SC2Replay')

    def test_init(self):
        self.assertEqual(self.replay.map, 'Toxic Slums')
        self.assertEqual(self.replay.duration, '26m 17s')
        self.assertEqual(self.replay.version, '1.0.2.16223')
        self.assertEqual(len(self.replay.players), 8)
