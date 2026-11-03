
# ==============================
# NETRUNNER CONFIGURATION
# ==============================

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
