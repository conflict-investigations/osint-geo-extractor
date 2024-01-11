import json
from io import BytesIO
from zipfile import ZipFile
from typing import Any

from .base import Downloader


ENCODING = 'utf-8'

# This is the Google Earth KML:
# https://cdn.geoconfirmed.org/geoconfirmed/kmls/ukraine-google-earth.kml
# Whose raw XML embeds this URL:
GEOCONFIRMED_ENDPOINT = 'https://geoconfirmed.org/api/map/ExportAsKml/Ukraine'  # noqa
# Data structure: Standard KML
# @Geoconfirmed - Ukraine - 21 2120 Dec 2023.zip
# ├── doc.kml
# └── images
#     ├── _CIRCLES_0051CA_UA_56_01.png
#     ├── ....png
GEOCONFIRMED_DOC_FILENAME = 'doc.kml'

# This is the "raw" KML which seems to be generated dynamically:
# blob:https://geoconfirmed.azurewebsites.net/d126ef8c-7f30-4928-86be-523429460377
# Old endpoint, no longer reachable
# https://geoconfirmed.azurewebsites.net/api/placemark/Ukraine

class GeoConfirmedDownloader(Downloader):
    """
    @GeoConfirmed
    Data from https://geoconfirmed.azurewebsites.net/
    with blessing from author
    """

    def download(self) -> Any:
        resp = self.request_url(GEOCONFIRMED_ENDPOINT)
        kml_zip = ZipFile(BytesIO(resp.read()))
        return kml_zip.open(GEOCONFIRMED_DOC_FILENAME).read().decode(ENCODING)
