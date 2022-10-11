import json
from urllib import request

from .base import Downloader

GEOCONFIRMED_ENDPOINT = 'https://geoconfirmed.azurewebsites.net/api/map/GetMap/Ukraine'  # noqa

ENCODING = 'utf-8'

class GeoConfirmedDownloader(Downloader):
    """
    @GeoConfirmed
    Data from https://geoconfirmed.azurewebsites.net/api/map/GetMap/Ukraine
    with blessing from author
    """

    @staticmethod
    def download():
        resp = request.urlopen(GEOCONFIRMED_ENDPOINT)
        data = json.loads(resp.read().decode(ENCODING))
        return data
