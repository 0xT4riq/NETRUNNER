
import socket


def get_registered_service(port):
    """
    Get the conventional service name registered
    for a TCP port number.
    """

    try:
        return socket.getservbyport(port, "tcp")

    except OSError:
        return "Unknown"


def detect_service(banner):
    """
    Make a basic guess based on the received banner.
    This is not full service fingerprinting.
    """

    if not banner:
        return "Unknown"

    upper_banner = banner.upper()

    if upper_banner.startswith("SSH-"):
        return "SSH"

    elif upper_banner.startswith("HTTP/"):
        return "HTTP"

    elif upper_banner.startswith("220"):
        return "FTP/SMTP (Possible)"

    elif upper_banner.startswith("+OK"):
        return "POP3"

    elif upper_banner.startswith("* OK"):
        return "IMAP"

    return "Unknown"
