import socket
import logging
from urllib.parse import urlparse


logger = logging.getLogger(__name__)

class GetIP:

    def __init__(self, domain):
        self.domain = domain

    def get_ip(self):
        try:
            host = urlparse(self.domain).netloc
            ip = socket.gethostbyname(host)
            response = {"hostname": host, "IP": ip}
            logger.info(f"Hostname: {host}")
            logger.info(f"IP: {ip}")

            return response

        except Exception as e:
            logger.error(f"Unable to get IP from domain: {str(e)}")
            return None
