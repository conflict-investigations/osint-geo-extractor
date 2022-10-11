from dataclasses import asdict, dataclass, field
from typing import List

@dataclass
class Event():
    id: str = None
    date: str = None
    latitude: float = None
    longitude: float = None
    place_desc: str = None
    title: str = None
    description: str = None
    sources: List['Source'] = field(default_factory=list)
    # Filters only relevant for Bellingcat entries
    filters: List['Association'] = field(default_factory=list)

    # https://www.delftstack.com/howto/python/dataclass-to-json-in-python/
    @property
    def __dict__(self):
        return asdict(self)

@dataclass
class Source():
    id: str
    path: str
    description: str

# Associations only relevant for Bellingcat entries
@dataclass
class Association():
    key: str
    value: str
