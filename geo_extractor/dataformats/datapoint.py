from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, List, Optional

# XXX: This might belong more in media_search than in geo_extractor

@dataclass
class Location():
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_desc: Optional[str] = None

@dataclass
class Datapoint():
    id: Optional[str] = None
    date: Optional[datetime] = None
    source: Optional[str] = None
    description: Optional[str] = None
    location: Optional[Location] = None

    # https://www.delftstack.com/howto/python/dataclass-to-json-in-python/
    # Return date as string when dumping to json
    @property
    def __dict__(self) -> Any:
        conv = asdict(self)
        conv['date'] = datetime.strftime(conv['date'], '%Y-%m-%d')
        return conv

@dataclass
class URLWithDatapoints():
    datapoints: List['Datapoint']
    url: Optional[str] = None

    @property
    def __dict__(self) -> Any:
        return asdict(self)
