import re

from src.repositories.location_finder import KNOWN_IPS


def test_known_ips_are_properly_formatted():
    ip_regexp = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"
    for ip in KNOWN_IPS:
        assert re.match(ip_regexp, ip)


def test_known_ips_locations_are_valid():
    location_regexp = r"^\d\_[\w\_]+$"
    for location in KNOWN_IPS.values():
        assert re.match(location_regexp, location)
