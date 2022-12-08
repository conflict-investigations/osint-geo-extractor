from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, List, Optional

@dataclass
class Event():
    id: Optional[str]
    date: datetime
    latitude: float
    longitude: float
    place_desc: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    links: List[str] = field(default_factory=list)

    @property
    def __dict__(self) -> Any:
        conv = asdict(self)
        conv['date'] = datetime.strftime(conv['date'], '%Y-%m-%d')
        return conv
