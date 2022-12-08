from datetime import datetime
from typing import List, Optional

from ..constants import SOURCE_NAMES
from ..dataformats import Event

link_extract_regex = r"(https?://.+?)([ ,\n\\<>]|$)"
entry_extract_regex = r"ENTRY: (\w+)[\n]?"

class CenInfoResExtractor():
    @staticmethod
    def extract_events(data, eventtype: str = None) -> List[Event]:
        # Input format is 2022-10-10T00:00:00 but only use date, not hours
        DATE_INPUT_FORMAT = '%Y-%m-%d'
        events = []

        def parse_date(d: str) -> Optional[datetime]:
            try:
                return datetime.strptime(d, DATE_INPUT_FORMAT)
            except ValueError:
                return None

        for feature in data['features']:
            props = feature.get('properties', {})
            if not props.get('description'):
                props['description'] = ''

            date = None
            if (date_raw := props.get('verifiedDate')):
                date = parse_date(date_raw[:10])

            # Description format has changed, no longer contains inline links
            sources = []  # type: List[str]
            if (url := props.get('url')):
                sources.append(url)

            entryid = props.get('id')

            latitude, longitude = [0.0, 0.0]
            geometry = feature.get('geometry')
            # We're parsing GeoJSON, swap lat/lng
            if geometry.get('type') == 'Point':
                longitude, latitude = geometry.get('coordinates')
            # We need floats, not strings
            latitude = float(latitude)
            longitude = float(longitude)

            country = props.get('country')
            province = props.get('province')
            city = props.get('city')
            place_desc = f"{country} - {province} - {city}"

            event = Event(
                id=entryid,
                date=date,
                latitude=latitude,
                longitude=longitude,
                place_desc=place_desc,
                title=props.get('title'),
                description=props['description'],
                links=sources,
                source=SOURCE_NAMES.CENINFORES,
            )
            events.append(event)

        return events
