from unittest import TestCase
from unittest.mock import patch

from hw31.calc import Calc


class TestCalc(TestCase):
    """Calc tests"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("")

    def test_add(self):
        """Add operation test"""
        print("id: " + self.id())
        self.assertEqual(Calc.add(1, 2), 3)

    def test_sub(self):
        """Sub operation test"""
        print("id: " + self.id())
        self.assertEqual(Calc.sub(4, 2), 2)

    def test_mul(self):
        """Mul operation test"""
        print("id: " + self.id())
        self.assertEqual(Calc.mul(2, 5), 10)

    def test_div(self):
        """Div operation test"""
        print("id: " + self.id())
        self.assertEqual(Calc.div(8, 4), 2)


class TestCalculator(TestCase):
    @patch('hw31.calc.Calc.add', return_value=9)
    def test_sum(self, add):
        """Wrong sum operation test"""
        self.assertEqual(add(2, 3), 9)
