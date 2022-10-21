from datetime import datetime
from typing import Any, List

from ..constants import SOURCE_NAMES
from ..dataformats import Event

class TextyExtractor():
    @staticmethod
    def extract_events(data: List[Any], eventtype: str = None) -> List[Event]:
        DATE_INPUT_FORMAT = '%Y-%m-%d'
        events = []
        for e in data:
            links = [link] if (link := e.get('link')) else []
            place = ' - '.join(filter(None,
                (e.get('address'), e.get('place'), e.get('oblast'))
            ))
            event = Event(
                id=None,  # no sane way to obtain stable ids from a spreadsheet
                date=datetime.strptime(e.get('date'), DATE_INPUT_FORMAT),
                latitude=float(e.get('latitude')),
                longitude=float(e.get('longitude')),
                place_desc=place,
                title=e.get('title'),
                source=SOURCE_NAMES.TEXTY,
                links=links,
            )
            events.append(event)
        return events
