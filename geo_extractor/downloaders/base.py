import json
import socket
import time
from typing import Any, Dict, Optional
from urllib import request
from urllib.error import HTTPError, URLError

ENCODING = 'utf-8'
USER_AGENT = 'media_search/0.0.1 - github.com/conflict-investigations/media-search-engine'  # noqa

MAX_RETRIES = 10
TIMEOUT = 60  # seconds
BACKOFF_FACTOR = 3  # seconds

# https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
# Algorithm:
# {backoff factor} * (2 ** ({number of total retries} - 1))
# For example, if the backoff factor is set to:
#  1 second the successive sleeps will be 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256
#  2 seconds - 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
#  10 seconds - 5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560

class Downloader():
    """
    Should return a dict of downloaded JSON, json.loads()-ed
    """
    def download(self) -> Any:
        raise NotImplementedError

    @staticmethod
    def request_url(url: str,
                    method: str = 'GET',
                    request_data: bytes = None,
                    headers: Dict[str, str] = None,
                    retries: int = MAX_RETRIES,
                    timeout: int = TIMEOUT) -> Any:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en',
        }
        headers.update(**headers)
        _req = request.Request(url=url, headers=headers, method=method)

        def _fetch(req: request.Request) -> str:
            with request.urlopen(req,
                                 data=request_data,
                                 timeout=timeout) as resp:
                return resp.read().decode(ENCODING)

        r = 0
        while r < retries:
            wait_time = BACKOFF_FACTOR * (2 ** (r - 1))
            try:
                return _fetch(_req)
            except HTTPError as e:
                r += 1
                print(f"HTTPError, retrying. e={e}")
                time.sleep(wait_time)
                continue
            except URLError as e:
                r += 1
                if isinstance(e.reason, socket.timeout):
                    print("Socket timeout, retrying")
                    continue
                print(f"URLError, retrying. e={e}")
                time.sleep(wait_time)
        # No success after max retries, raise error:
        raise HTTPError(code=429, reason='Too many retries', headers=None)
