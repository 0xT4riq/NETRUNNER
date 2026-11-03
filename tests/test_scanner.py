import unittest
import socket
import threading

from core.scanner import scan


class TestScanner(unittest.TestCase):

    def test_detect_open_local_port(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)

        port = server.getsockname()[1]

        def handle_connection():
            try:
                conn, _ = server.accept()
                with conn:
                    conn.sendall(b"SSH-2.0-TestServer\r\n")
            except OSError:
                pass

        thread = threading.Thread(target=handle_connection)
        thread.start()

        try:
            results = scan(
                "127.0.0.1",
                "localhost",
                port,
                port
            )

            self.assertEqual(len(results["open_ports"]), 1)
            self.assertEqual(
                results["open_ports"][0]["port"],
                port
            )

        finally:
            server.close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()