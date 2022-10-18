import json
import socket
import time
from typing import Any, Dict, Optional
from urllib import request
from urllib.error import HTTPError, URLError

ENCODING = 'utf-8'
USER_AGENT = 'media_search/0.0.1 - github.com/conflict-investigations/media-search-engine'  # noqa

TIMEOUT = 60
MAX_RETRIES = 5

class Downloader():
    """
    Should return a dict of downloaded JSON, json.loads()-ed
    """
    def download(self) -> Any:
        raise NotImplementedError

    @staticmethod
    def request_json(url: str,
                     method: str = 'GET',
                     request_data: Optional[bytes] = None,
                     headers: Optional[Dict[str, str]] = None,
                     retries: Optional[int] = MAX_RETRIES,
                     timeout: Optional[int] = TIMEOUT) -> Any:
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

        def _fetch_as_json(req: request.Request) -> Any:
            return json.loads(_fetch(req))

        r = 0
        while r < retries:
            try:
                return _fetch_as_json(_req)
            except HTTPError as e:
                r += 1
                print(f"HTTPError, retrying. e={e}")
                time.sleep(60)
                continue
            except URLError as e:
                r += 1
                if isinstance(e.reason, socket.timeout):
                    print("Socket timeout, retrying")
                    continue
                print(f"URLError, retrying. e={e}")
                time.sleep(10)
        raise HTTPError
