import unittest
import sys
from unittest.mock import MagicMock
sys.modules["numpy"] = MagicMock()

from src.nethawk.components.status import Status

class TestStatusValidation(unittest.TestCase):
    def test_valid_status(self):
        # Should not raise any exceptions
        status = Status(
            hp=10, max_hp=10, power=5, max_power=5, ac=10, level=1, gold=100, exp=0, hunger=0
        )
        self.assertEqual(status.max_hp, 10)
        self.assertEqual(status.max_power, 5)
        self.assertEqual(status.level, 1)
        self.assertEqual(status.gold, 100)
        self.assertEqual(status.exp, 0)

    def test_invalid_max_hp(self):
        with self.assertRaises(ValueError):
            Status(hp=0, max_hp=0, power=5, max_power=5, ac=10, level=1, gold=100, exp=0, hunger=0)

    def test_invalid_max_power(self):
        with self.assertRaises(ValueError):
            Status(hp=10, max_hp=10, power=-1, max_power=-1, ac=10, level=1, gold=100, exp=0, hunger=0)

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            Status(hp=10, max_hp=10, power=5, max_power=5, ac=10, level=0, gold=100, exp=0, hunger=0)

    def test_invalid_gold(self):
        with self.assertRaises(ValueError):
            Status(hp=10, max_hp=10, power=5, max_power=5, ac=10, level=1, gold=-10, exp=0, hunger=0)

    def test_invalid_exp(self):
        with self.assertRaises(ValueError):
            Status(hp=10, max_hp=10, power=5, max_power=5, ac=10, level=1, gold=100, exp=-50, hunger=0)

if __name__ == '__main__':
    unittest.main()
