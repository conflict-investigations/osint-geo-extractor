import re
from datetime import datetime
from typing import List, Optional

from ..constants import SOURCE_NAMES
from ..dataformats import Event

link_extract_regex = r"(https?://.+?)([ ,\n\\<>]|$)"
entry_extract_regex = r"ENTRY: (\w+)[\n]?"

class CenInfoResExtractor():
    @staticmethod
    def extract_events(data, eventtype: str = None) -> List[Event]:
        DATE_INPUT_FORMAT = '%d/%m/%Y'
        events = []

        def parse_date(d: str) -> Optional[datetime]:
            try:
                return datetime.strptime(d, DATE_INPUT_FORMAT)
            except ValueError:
                return None

        for feature in data['geojson']['features']:
            props = feature.get('properties', {})
            if not props.get('description'):
                props['description'] = ''

            date = None
            if (date_raw := props.get('title')):
                date = parse_date(date_raw[:10])

            links = []  # type: List[str]
            if (url := props.get('media_url')):
                links.append(url)
            if (matches := re.findall(link_extract_regex,
                                      props['description'])):
                links.extend((link for link, _unused in matches))

            # Remove duplicate URLs
            sources = list(set(links))  # type: List[str]

            entryid = None
            if (candidate := re.findall(entry_extract_regex,
                                        props['description'])):
                entryid = candidate[0]

            latitude, longitude = [0.0, 0.0]
            geometry = feature.get('geometry')
            # We're parsing GeoJSON, swap lat/lng
            if geometry.get('type') == 'Point':
                longitude, latitude = geometry.get('coordinates')
            elif geometry.get('type') == 'LineString':
                # Be lazy and use first vector of LineString
                longitude, latitude = geometry.get('coordinates')[0]
            # We need floats, not strings
            latitude = float(latitude)
            longitude = float(longitude)

            event = Event(
                id=entryid,
                date=date,
                latitude=latitude,
                longitude=longitude,
                place_desc=None,
                title=props.get('title'),
                description=props['description'],
                links=sources,
                source=SOURCE_NAMES.CENINFORES,
            )
            events.append(event)

        return events
