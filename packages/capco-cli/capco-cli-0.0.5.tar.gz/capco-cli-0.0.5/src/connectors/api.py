import requests


class RestApiRunner:

    DEFAULT_TIMEOUT = 30
    DEFAULT_HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, base_uri, user, password, headers=None, timeout=None):
        self.base_uri = base_uri
        self.auth = (user, password)
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout or self.DEFAULT_TIMEOUT

    def get(self, uri):
        response = requests.get(url=self._complete_uri(uri), auth=self.auth, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response

    def _complete_uri(self, uri):
        return '/'.join([self.base_uri, uri])
