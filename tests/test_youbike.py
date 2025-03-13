import unittest

import youbike


class TestYouBike(unittest.TestCase):

    def test_youbike(self):
        data = youbike.getallstations()
        self.assertIsInstance(data, list, "getallstations() should return a list")


if __name__ == '__main__':
    unittest.main()
