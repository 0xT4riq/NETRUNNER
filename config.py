
# ==============================
# NETRUNNER CONFIGURATION
# ==============================


VERSION = "1.1.0"

# Scanner settings
MAX_WORKERS = 100

# Network timeouts (seconds)
CONNECT_TIMEOUT = 1
BANNER_TIMEOUT = 0.7

# HTTP probing
HTTP_PORTS = {
    80,
    8000,
    8008,
    8080,
    8888
}

# Default scan range
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 65535



# Port profiles
PORT_PROFILES = {
    "quick": [
        21, 22, 23, 25, 53, 80, 110, 111, 135,
        139, 143, 443, 445, 993, 995, 1723,
        3306, 3389, 5900, 8080
    ],

    "web": [
        80, 443, 8000, 8008, 8080, 8081,
        8443, 8888, 9000, 9090, 9443
    ],

    "full": list(range(1, 65536))
}