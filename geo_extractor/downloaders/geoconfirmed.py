import json
from typing import Any

from .base import Downloader

GEOCONFIRMED_ENDPOINT = 'https://geoconfirmed.azurewebsites.net/api/map/GetMap/Ukraine'  # noqa

class GeoConfirmedDownloader(Downloader):
    """
    @GeoConfirmed
    Data from https://geoconfirmed.azurewebsites.net/api/map/GetMap/Ukraine
    with blessing from author
    """

    def download(self) -> Any:
        return json.loads(self.request_url(GEOCONFIRMED_ENDPOINT))
