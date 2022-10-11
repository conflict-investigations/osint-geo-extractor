import json
from urllib import request

from .base import Downloader

CENINFORES_JSON_URL = 'https://maphub.net/json/map_load/176607'
# It seems maphub blocks 'python-urllib' user agent, so set an innocent one
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'  # noqa

ENCODING = 'utf-8'
TIMEOUT = 20

class CenInfoResDownloader(Downloader):
    """
    Centre for Information Resilience
    Data from https://maphub.net/Cen4infoRes/russian-ukraine-monitor
    """

    @staticmethod
    def download():
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT,
        }
        req = request.Request(
            url=CENINFORES_JSON_URL,
            headers=headers,
            method='POST',
        )
        return json.loads(
            request.urlopen(
                req,
                # data=json.dumps({}).encode('utf-8'),
                data=b'{}',
                timeout=TIMEOUT,
            ).read().decode(ENCODING)
        )
