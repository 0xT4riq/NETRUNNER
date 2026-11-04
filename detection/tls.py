import socket
import ssl
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.primitives import hashes



def inspect_tls(hostname, port=443, timeout=5):
    result = {
        "hostname": hostname,
        "port": port,
        "tls_supported": False,
        "tls_version": None,
        "cipher": None,
        "certificate": None,
        "certificate_verified": None,
        "verification_error": None,
        "error": None
    }

    try:
        context = ssl.create_default_context()

        try:
            with socket.create_connection(
                (hostname, port), timeout=timeout
            ) as sock:
                with context.wrap_socket(
                    sock, server_hostname=hostname
                ) as tls_sock:
                    certificate_der = tls_sock.getpeercert(binary_form=True)
                    result["certificate_verified"] = True

                    result["tls_version"] = tls_sock.version()

                    cipher_info = tls_sock.cipher()
                    result["cipher"] = cipher_info[0] if cipher_info else None

        except ssl.SSLCertVerificationError as exc:
            result["certificate_verified"] = False
            result["verification_error"] = str(exc)

            # Retry without certificate verification
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection(
                (hostname, port), timeout=timeout
            ) as sock:
                with context.wrap_socket(
                    sock, server_hostname=hostname
                ) as tls_sock:
                    certificate_der = tls_sock.getpeercert(binary_form=True)
                    result["certificate_verified"] = False

                    result["tls_version"] = tls_sock.version()

                    cipher_info = tls_sock.cipher()
                    result["cipher"] = cipher_info[0] if cipher_info else None

        result["tls_supported"] = True
        
        

        if not certificate_der:
            result["error"] = "Server did not provide a certificate."
            return result
        
        
        now = datetime.now(timezone.utc)

        certificate = x509.load_der_x509_certificate(
            certificate_der
        )
        if now < certificate.not_valid_before_utc:
            status = "Not Yet Valid"

        elif now > certificate.not_valid_after_utc:
            status = "Expired"

        else:
            status = "Valid"



        try:
            san_extension = certificate.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )
            san_domains = san_extension.value.get_values_for_type(
                x509.DNSName
            )
        except x509.ExtensionNotFound:
            san_domains = []

        fingerprint = certificate.fingerprint(hashes.SHA256()).hex()
        remaining = certificate.not_valid_after_utc - now
        days_remaining = remaining.days
        result["certificate"] = {
            "subject": certificate.subject.rfc4514_string(),
            "issuer": certificate.issuer.rfc4514_string(),
            "valid_from": str(certificate.not_valid_before_utc),
            "valid_until": str(certificate.not_valid_after_utc),
            "validity_status": status,
            "san_domains": san_domains,
            "fingerprint_sha256": fingerprint,
            "days_remaining": days_remaining
        }

    except (OSError, ssl.SSLError, ValueError) as exc:
        result["error"] = str(exc)

    return result