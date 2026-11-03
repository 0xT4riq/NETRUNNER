import unittest
from unittest.mock import patch
import socket

from core.target import check_ip


class TestTargetValidation(unittest.TestCase):

    def test_valid_ipv4(self):
        self.assertEqual(check_ip("127.0.0.1"), "127.0.0.1")

    @patch("core.target.socket.gethostbyname", return_value="93.184.216.34")
    def test_valid_hostname(self, mock_dns):
        result = check_ip("example.com")

        self.assertEqual(result, "93.184.216.34")
        mock_dns.assert_called_once_with("example.com")

    @patch("core.target.socket.gethostbyname", side_effect=socket.gaierror)
    def test_invalid_hostname(self, mock_dns):
        with self.assertRaises(ValueError):
            check_ip("invalid-hostname")

    def test_invalid_ip_format(self):
        with patch("core.target.socket.gethostbyname",
                   side_effect=socket.gaierror):
            with self.assertRaises(ValueError):
                check_ip("999.999.999.999")


if __name__ == "__main__":
    unittest.main()