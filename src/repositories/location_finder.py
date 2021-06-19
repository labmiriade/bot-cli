from typing import Optional

from requests import request

KNOWN_IPS = {
    "94.141.5.74": "2_Thiene",
    "5.157.117.184": "2_Thiene",
    "185.4.153.8": "1_Padova",
}


def current_location() -> Optional[str]:
    """
    Returns the current location of the user based on known IP addresses
    @return: the location of the user if the IP is known, None otherwise
    """
    ip = request("GET", "https://ipecho.net/plain").text
    return KNOWN_IPS.get(ip)
