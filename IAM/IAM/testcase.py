def Multiit(x,y):
    return  x*y

import unittest

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('hii thiss is login ')
    def setUp(self):
        print('this is set up')
    def test_positive(self):
        x = 5
        y = 4
        result = Multiit(x, y)
        self.assertEqual(result, 20)
        print('this is positive')
    def test_negative(self):
        x = -5
        y = 4
        result = Multiit(x, y)
        self.assertEqual(result, -20)
        print('this is negative')
    def tearDown(self):
        print('this is for teardown')
    @classmethod
    def tearDownClass(cls):
        print('thihs is for temp database ')


if __name__ == '__main__':
    unittest.main()
