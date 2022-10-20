import json
from typing import Any

from .base import Downloader

DEFMON_ENDPOINT = 'https://widgets.scribblemaps.com/api/maps/nBT8ffpeGH/smjsonLocal'  # noqa

# TODO: "Archived" map with older entries
# https://www.scribblemaps.com/maps/view/Operational%20Map%20Ukraine%20(copy)/19bUdxmFGh
# https://www.scribblemaps.com/api/maps/19bUdxmFGh/smjson?cb=1665511749093

class DefmonDownloader(Downloader):

    def download(self) -> Any:
        return json.loads(self.request_url(DEFMON_ENDPOINT))
