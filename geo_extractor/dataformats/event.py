from dataclasses import asdict, dataclass, field
from datetime import datetime

@dataclass
class Event():
    id: str = None
    date: datetime = None
    latitude: float = None
    longitude: float = None
    place_desc: str = None
    title: str = None
    description: str = None
    source: str = None
    links: list = field(default_factory=list)

    @property
    def __dict__(self):
        conv = asdict(self)
        conv['date'] = datetime.strftime(conv['date'], '%Y-%m-%d')
        return conv
