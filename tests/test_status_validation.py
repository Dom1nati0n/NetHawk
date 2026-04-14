import unittest
from src.nethawk.components.status import Status

class TestStatusValidation(unittest.TestCase):
    def test_valid_status(self):
        status = Status(
            hp=10,
            max_hp=10,
            power=5,
            max_power=5,
            ac=10,
            level=1,
            gold=0,
            exp=0,
            hunger=1
        )
        self.assertEqual(status.hp, 10)

    def test_invalid_hp(self):
        with self.assertRaises(ValueError):
            Status(
                hp=-10,
                max_hp=10,
                power=5,
                max_power=5,
                ac=10,
                level=1,
                gold=0,
                exp=0,
                hunger=1
            )

    def test_invalid_type_bool(self):
        with self.assertRaises(TypeError):
            Status(
                hp=True,
                max_hp=10,
                power=5,
                max_power=5,
                ac=10,
                level=1,
                gold=0,
                exp=0,
                hunger=1
            )

    def test_invalid_type_float(self):
        with self.assertRaises(TypeError):
            Status(
                hp=10.5,
                max_hp=10,
                power=5,
                max_power=5,
                ac=10,
                level=1,
                gold=0,
                exp=0,
                hunger=1
            )

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            Status(
                hp=10,
                max_hp=10,
                power=5,
                max_power=5,
                ac=10,
                level=0,
                gold=0,
                exp=0,
                hunger=1
            )

if __name__ == '__main__':
    unittest.main()
