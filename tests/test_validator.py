
import unittest

from core.validator import validate_port_range


class TestPortValidator(unittest.TestCase):

    def test_valid_range(self):
        validate_port_range(1, 1000)

    def test_single_port(self):
        validate_port_range(80, 80)

    def test_start_port_too_low(self):
        with self.assertRaises(ValueError):
            validate_port_range(0, 100)

    def test_end_port_too_high(self):
        with self.assertRaises(ValueError):
            validate_port_range(1, 65536)

    def test_start_greater_than_end(self):
        with self.assertRaises(ValueError):
            validate_port_range(1000, 80)


if __name__ == "__main__":
    unittest.main()
