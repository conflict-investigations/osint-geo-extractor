import csv
import io
from datetime import datetime
from typing import List, Optional

from ..constants import SOURCE_NAMES
from ..dataformats import Event

class DefmonSpreadsheetExtractor():

    @staticmethod
    def extract_events(data: str, eventtype: str = None) -> List[Event]:
        proxy = io.StringIO(data)  # Emulate real file to be read line by line
        next(proxy)  # Skip first row
        csv_reader = csv.reader(proxy, delimiter=',')
        # Transpose rows and columns via zip():
        zipped = list(zip(*csv_reader))

        location_mapping = []

        cities = zipped[6]
        latitudes = zipped[7]
        longitudes = zipped[8]
        for pos, item in enumerate(cities):
            if pos == 0:
                continue  # skip headers
            location_mapping.append(
                (item, latitudes[pos], longitudes[pos])
            )

        DATE_INPUT_FORMAT = '%Y%m%d'

        def _date(date_string: str) -> Optional[datetime]:
            try:
                return datetime.strptime(date_string, DATE_INPUT_FORMAT)
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
                loc = location_mapping[pos]
                locations.append(Event(
                    id=None,
                    date=_date(day[0]),
                    latitude=float(loc[1]),
                    longitude=float(loc[2]),
                    place_desc=loc[0],
                    title=None,
                    description=None,
                    links=[],
                    source=SOURCE_NAMES.DEFMON,
                ))
            events.extend(locations)

        return events
