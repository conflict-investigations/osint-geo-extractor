import csv
import io
from datetime import datetime
from typing import List, Optional, Tuple

from ..constants import FALLBACK_DATE, SOURCE_NAMES
from ..dataformats import Event

class DefmonSpreadsheetExtractor():

    @staticmethod
    def extract_events(data: str) -> List[Event]:
        proxy = io.StringIO(data)  # Emulate real file to be read line by line
        next(proxy)  # Skip first row
        csv_reader = csv.reader(proxy, delimiter=',')
        # Transpose rows and columns via zip():
        zipped = list(zip(*csv_reader))

        location_mapping = []

        cities = zipped[6]
        alternate_names = zipped[5]
        latitudes = zipped[7]
        longitudes = zipped[8]
        for pos, item in enumerate(cities):
            if pos == 0:
                continue  # skip headers
            location_mapping.append(
                (item, alternate_names[pos], latitudes[pos], longitudes[pos])
            )

        DATE_INPUT_FORMAT = '%Y%m%d'

        def _date(date_string: str) -> datetime:
            try:
                return datetime.strptime(date_string, DATE_INPUT_FORMAT)
            except ValueError:
                # Input string was invalid:
                return FALLBACK_DATE

        def _backup_coords(place_name: str) -> Optional[
                Tuple[float, float]]:
            """
            Fetch coordinates from other entry with same place name
            """
            try:
                pos = cities.index(place_name)
                return (latitudes[pos], longitudes[pos])
            except ValueError:
                return None

        events = []
        for day in zipped:
            if not day[0].startswith('202'):  # 20220623, 20230101, ...
                continue  # skip columns which are not daily data
            locations = []
            for pos, item in enumerate(day[1:]):
                if not item:
                    # Skip non-'X' entries
                    continue
                place_name, alternate_name, lat, lng = location_mapping[pos]
                desc = None
                if alternate_name:
                    desc = 'Alternate place names: %s' % alternate_name
                if not all((lat, lng)):
                    # Fetch coordinates from other entry with same place name
                    lat, lng = _backup_coords(place_name) or (None, None)
                    desc = ', '.join(filter(None,
                               [desc, 'coordinates imprecise'])).capitalize()
                if not all((lat, lng)):
                    # Skip entries without coordinates
                    continue
                locations.append(Event(
                    id=None,
                    date=_date(day[0]),
                    latitude=float(lat),
                    longitude=float(lng),
                    place_desc=place_name,
                    title='Shelling at %s' % place_name,
                    description=desc,
                    links=[],
                    source=SOURCE_NAMES.DEFMON,
                ))
            events.extend(locations)

        return events
