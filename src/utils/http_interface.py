import logging
import urllib.request


logger = logging.getLogger(__name__)

class GetPage:

    def __init__(self, domain, port, uri=""):
        self.domain = domain
        self.port = port
        self.uri = uri

    def get_page(self):
        _uri = ""
        try:
            if self.uri:
                _uri = f"/{self.uri}"
            endpoint = f"{self.domain}{_uri}:{self.port}"

            request = urllib.request.Request(endpoint)
            response = urllib.request.urlopen(request)
            logger.info(f"Domain: {self.domain}")
            logger.info(f"Port: {self.port}")

            return response.read().decode(encoding="utf-8")

        except Exception as e:
            logger.error(f"Unable to get the page {str(e)}")
            return None
