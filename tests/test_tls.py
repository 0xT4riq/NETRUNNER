import unittest

from detection.tls import inspect_tls
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

def generate_test_certificate():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    subject = x509.Name([
        x509.NameAttribute(
            NameOID.COMMON_NAME, "example.com"
        )
    ])

    now = datetime.now(timezone.utc)

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=30))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("example.com")
            ]),
            critical=False
        )
        .sign(key, hashes.SHA256())
    )

    return certificate.public_bytes(serialization.Encoding.DER)

class TestTLSInspection(unittest.TestCase):

    @patch("detection.tls.socket.create_connection")
    def test_connection_failure(self, mock_connection):
        mock_connection.side_effect = OSError("Connection refused")

        result = inspect_tls("example.com")

        self.assertFalse(result["tls_supported"])
        self.assertEqual(result["error"], "Connection refused")
        self.assertIsNone(result["certificate"])

    @patch("detection.tls.socket.create_connection")
    def test_invalid_hostname(self, mock_connection):
        mock_connection.side_effect = OSError("DNS resolution failed")

        result = inspect_tls("invalid.example")

        self.assertFalse(result["tls_supported"])
        self.assertEqual(result["error"], "DNS resolution failed")
        
    @patch("detection.tls.ssl.create_default_context")
    @patch("detection.tls.socket.create_connection")
    def test_successful_tls_inspection(
        self, mock_connection, mock_context
    ):
        certificate_der = generate_test_certificate()

        # Simulate TCP socket
        tcp_socket = MagicMock()
        tcp_socket.__enter__.return_value = tcp_socket

        mock_connection.return_value = tcp_socket

        # Simulate TLS socket
        tls_socket = MagicMock()
        tls_socket.__enter__.return_value = tls_socket

        tls_socket.getpeercert.return_value = None
        tls_socket.getpeercert.return_value = certificate_der

        tls_socket.version.return_value = "TLSv1.3"
        tls_socket.cipher.return_value = (
            "TLS_AES_256_GCM_SHA384",
            "TLSv1.3",
            256
        )

        context = mock_context.return_value
        context.wrap_socket.return_value = tls_socket

        result = inspect_tls("example.com")

        self.assertTrue(result["tls_supported"])
        self.assertTrue(result["certificate_verified"])
        self.assertEqual(result["tls_version"], "TLSv1.3")
        self.assertEqual(result["cipher"], "TLS_AES_256_GCM_SHA384")

        self.assertEqual(
            result["certificate"]["subject"],
            "CN=example.com"
        )

        self.assertIn(
            "example.com",
            result["certificate"]["san_domains"]
        )


if __name__ == "__main__":
    unittest.main()