import re
from datetime import datetime
from typing import Any, List

from ..constants import FALLBACK_DATE, FALLBACK_DATE_STR, SOURCE_NAMES
from ..dataformats import Event

link_extract_regex = r"(https?://.+?)([ ,\n\\<>]|$)"

class GeoConfirmedExtractor():
    @staticmethod
    def extract_events(data: Any) -> List[Event]:

        events: List[Event] = []

        # Example: "2022-10-10T16:20:00"
        DATE_INPUT_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

        def parse_date(d: str) -> datetime:
            # Note: e.g. twitter.com/GeoConfirmed/status/1579567301963440128
            # has a wrong date (twitter id instead of date string)
            try:
                return datetime.strptime(d, DATE_INPUT_FORMAT)
            except ValueError:
                # Input string was invalid:
                # return FALLBACK_DATE
                return None

        def find_links(text: str, sources: List[str]) -> List[str]:
            if (links := re.findall(link_extract_regex, text)):
                return [link for link, _unused in links
                        if link not in sources]
            return []

        for item in data:

            if not item.get('description'):
                # Items without description are mostly left over
                # mapDataPlacemarks, which we discarded previously anyway
                continue

            sources = []  # type: List[str]

            if (src := item.get('originalSource')):
                if not src.startswith('http'):
                    sources.extend(find_links(src, sources))
                else:
                    sources.append(src)
            if (geo := item.get('geolocation')):
                if not geo.startswith('http'):
                    sources.extend(find_links(geo, sources))
                else:
                    sources.append(geo)

            sources.extend(find_links(item.get('description'), sources))

            if not sources:
                # This library is used to look up links, so discard items
                # which do not provide a source link
                continue

            desc: str = ' - '.join([
                    item.get('description'),
                    item.get('name'),
            ])

            event = Event(
                id=item.get('id'),
                date=parse_date(item.get('date')),
                # Coordinates (no longer) swapped
                latitude=float(item.get('coordinates')[0]),
                longitude=float(item.get('coordinates')[1]),
                place_desc=None,
                title=item.get('name'),
                description=desc,
                links=sources,
                source=SOURCE_NAMES.GEOCONFIRMED,
            )
            # XXX REMOVEME ugly hack for faulty GeoConfirmed data
            # e.g. dates like 1527-02-04T18:23:00
            if event.date < datetime(2000, 1, 1):
                event.date = FALLBACK_DATE
            events.append(event)

        return events
