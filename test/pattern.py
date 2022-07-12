import unittest
import numpy as np
from lifelike import Pattern

class TestGlider(unittest.TestCase):
    def setUp(self):
        self.pattern = Pattern('glider')

    def test_dimensions(self):
        self.assertEqual(self.pattern.x, 3)
        self.assertEqual(self.pattern.y, 3)

    def test_rle(self):
        self.assertEqual(self.pattern.rle, 'bob$2bo$3o!')

    def test_rule(self):
        self.assertEqual(self.pattern.rule, 'B3/S23')

    def test_decoding(self):
        U = np.array([[0,1,0],[0,0,1],[1,1,1]])
        self.assertTrue((self.pattern.U==U).all())


if __name__ == '__main__':
    unittest.main()
