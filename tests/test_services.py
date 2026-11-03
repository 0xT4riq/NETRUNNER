
import unittest

from detection.services import detect_service


class TestServiceDetection(unittest.TestCase):

    def test_ssh_detection(self):
        banner = "SSH-2.0-OpenSSH_9.0"
        self.assertEqual(detect_service(banner), "SSH")

    def test_http_detection(self):
        banner = "HTTP/1.1 200 OK"
        self.assertEqual(detect_service(banner), "HTTP")

    def test_pop3_detection(self):
        banner = "+OK POP3 server ready"
        self.assertEqual(detect_service(banner), "POP3")

    def test_imap_detection(self):
        banner = "* OK IMAP server ready"
        self.assertEqual(detect_service(banner), "IMAP")

    def test_unknown_service(self):
        banner = "Some random service"
        self.assertEqual(detect_service(banner), "Unknown")

    def test_empty_banner(self):
        self.assertEqual(detect_service(""), "Unknown")


if __name__ == "__main__":
    unittest.main()
