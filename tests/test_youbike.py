import unittest

import youbike


class TestYouBike(unittest.TestCase):

    def test_youbike(self):
        data = youbike.getdata()
        self.assertIsInstance(data, list, "getdata() should return a list")


if __name__ == '__main__':
    unittest.main()
