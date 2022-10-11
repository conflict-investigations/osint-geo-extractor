from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

# XXX: This might belong more in media_search than in geo_extractor

@dataclass
class Location():
    latitude: float
    longitude: float
    place_desc: str

@dataclass
class Datapoint():
    id: str
    date: datetime
    source: str
    description: str
    location: Location

    # https://www.delftstack.com/howto/python/dataclass-to-json-in-python/
    # Return date as string when dumping to json
    @property
    def __dict__(self):
        conv = asdict(self)
        conv['date'] = datetime.strftime(conv['date'], '%Y-%m-%d')
        return conv

@dataclass
class URLWithDatapoints():
    url: str
    datapoints: List['Datapoint']

    @property
    def __dict__(self):
        return asdict(self)
