import json
from typing import Any

from .base import Downloader

CENINFORES_GEOJSON_ENDPOINT = 'https://eyesonrussia.org/events.geojson'

# Old maphub integration, left for posterity's sake
CENINFORES_MAPHUB_JSON_ENDPOINT = 'https://maphub.net/json/map_load/176607'
# It seems maphub blocks 'python-urllib' user agent, so set an innocent one
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'  # noqa

class CenInfoResDownloader(Downloader):
    """
    Centre for Information Resilience
    Data from https://maphub.net/Cen4infoRes/russian-ukraine-monitor
    """

    def download(self) -> Any:
        return json.loads(self.request_url(CENINFORES_GEOJSON_ENDPOINT))
