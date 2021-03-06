#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 20.01.2017

:author: Paul Pasler
:organization: Reutlingen University
'''

from base_test import *  # @UnusedWildImport
from posdbos.source.dummy_data_source import DummyPacketSource, DummyWindowSource, DummyDataSource


class TestDummyDataSource(BaseTest):

    def setUp(self):
        self.source = DummyDataSource()
        self.source.convert()

    def test_defaults(self):
        self.assertNotEqual(self.source.filePath, None)
        self.assertTrue(self.source.infinite)

    def test_hasQuality(self):
        self.source._hasQuality()
        self.assertTrue(self.source.hasQuality)

        self.source.header = [head for head in self.source.header if not head.startswith("Q")]
        self.source._hasQuality()
        self.assertFalse(self.source.hasQuality)

class TestDummyPacketSource(BaseTest):

    def setUp(self):
        self.source = DummyPacketSource(self.getData32CSV(), False)
        self.source.convert()

    def test_convert_sunshine(self):
        self.assertTrue(self.source.hasMore)
        for _ in range(0, len(self.source.data)):
            self.source.dequeue()
        self.assertFalse(self.source.hasMore)

    def test_convert_several(self):
        for i in range(1, 3):
            source = DummyPacketSource([self.getData32CSV()]*i, False)
            source.convert()

            self.assertEqual(len(source.data), 32*i)
            for _ in range(0, len(source.data)):
                source.dequeue()
            self.assertFalse(source.hasMore)

    def test_dequeue(self):
        data = self.source.dequeue() 
        self.assertEquals(len(data.sensors), 17)
        self.assertTrue("X" in data.sensors.keys())
        self.assertTrue("quality" in data.sensors["X"].keys())

class TestDummyWindowSource(BaseTest):

    def setUp(self):
        self.source = DummyWindowSource(self.getData1024CSV(), False, 1, 2)
        self.source.convert()

    def test_convert_sunshine(self):
        self.assertTrue(self.source.hasMore)
        for _ in range(0, len(self.source.data)):
            self.source.dequeue()
        self.assertFalse(self.source.hasMore)

    def test_dequeue(self):
        data = self.source.dequeue() 

        self.assertEquals(len(data), 16)
        self.assertTrue("X" in data)
        self.assertTrue("quality" in data["X"].keys())

    def test__buildDataStructure_normal(self):
        self.source.data = []
        self.source._buildDataStructure()
        data = self.source.data
        windowSize = self.source.windowSize

        self.assertEqual(len(data), 15)
        self.assertEqual(len(data[0]["AF3"]["value"]), windowSize)

    def test__buildDataStructure_several(self):
        for i in range(1, 3):
            source = DummyWindowSource([self.getData1024CSV()]*i, False, 1, 2)
            source.convert()
            data = source.data
            windowSize = source.windowSize
    
            self.assertEqual(len(data), 15*i)
            self.assertEqual(len(data[0]["AF3"]["value"]), windowSize)

    def _getWindows(self, windowSeconds, windowCount, samplingRate):
        self.source.data = []
        self.source.windowSeconds = windowSeconds
        self.source.windowCount = windowCount
        self.source.samplingRate = samplingRate

        self.source._buildDataStructure()
        data = self.source.data
        windowSize = self.source.windowSize
        return data, windowSize

    def test__buildDataStructure(self):
        data, windowSize = self._getWindows(1, 4, 4)

        self.assertEqual(len(data), 1021)
        self.assertEqual(len(data[0]["AF3"]["value"]), windowSize)

if __name__ == '__main__':
    unittest.main()
