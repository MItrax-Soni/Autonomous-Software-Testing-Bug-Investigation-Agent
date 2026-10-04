import ipaddress
import socket
from urllib.parse import urlparse
from typing import Tuple
from app.config import settings

# CIDR networks that are prohibited to prevent SSRF
PROHIBITED_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),   # Link-local / Cloud metadata (AWS 169.254.169.254)
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("224.0.0.0/4"),     # Multicast
    ipaddress.ip_network("240.0.0.0/4"),
    # IPv6 prohibited
    ipaddress.ip_network("::1/128"),          # Loopback
    ipaddress.ip_network("fc00::/7"),         # Unique local
    ipaddress.ip_network("fe80::/10"),        # Link-local
]

class SSRFSecurityError(Exception):
    pass

class SSRFValidator:
    @staticmethod
    def validate_url(target_url: str) -> Tuple[bool, str]:
        """
        Validates target URL syntax and ensures resolved IP is not in prohibited private/metadata ranges.
        Returns (is_valid, error_or_success_message).
        """
        if not target_url or not isinstance(target_url, str):
            raise SSRFSecurityError("Target URL must be a non-empty string.")

        parsed = urlparse(target_url)

        # 1. Scheme Validation
        if parsed.scheme.lower() not in ("http", "https"):
            raise SSRFSecurityError(f"Prohibited URL scheme '{parsed.scheme}'. Only 'http' and 'https' are allowed.")

        hostname = parsed.hostname
        if not hostname:
            raise SSRFSecurityError("Invalid URL: missing hostname.")

        port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)

        # 2. Check for Controlled Local Defective Test App exemption
        if settings.SSRF_ALLOW_CONTROLLED_LOCAL_APP:
            if hostname in ("localhost", "127.0.0.1") and port == settings.CONTROLLED_LOCAL_APP_PORT:
                return True, "Permitted controlled local test target"

        if not settings.SSRF_PROTECTION_ENABLED:
            return True, "SSRF protection disabled via configuration"

        # 3. DNS Pre-Flight Resolution
        try:
            addr_info = socket.getaddrinfo(hostname, port, proto=socket.IPPROTO_TCP)
        except socket.gaierror as e:
            raise SSRFSecurityError(f"DNS resolution failure for host '{hostname}': {str(e)}")

        # 4. CIDR Deny-List Check for every resolved IP
        for family, _, _, _, sockaddr in addr_info:
            ip_str = sockaddr[0]
            try:
                ip_obj = ipaddress.ip_address(ip_str)
            except ValueError:
                raise SSRFSecurityError(f"Malformed IP address resolved: '{ip_str}'")

            for net in PROHIBITED_NETWORKS:
                if ip_obj in net:
                    raise SSRFSecurityError(
                        f"SSRF Protection: Host '{hostname}' resolved to prohibited IP '{ip_str}' in restricted network {net}."
                    )

        return True, "URL passed SSRF security validation."
