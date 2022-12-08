from datetime import datetime
from typing import Any, List

from ..constants import SOURCE_NAMES
from ..dataformats import Event

# "name": "War in Ukraine",
# "id": "f4a2b60dad",
WAR_IN_UKRAINE_ID = 'f4a2b60dad'

# Data format of DefMon3 map JSON is dictated by scribblemaps.com schema
# Divided into "folders" which then have sub-folders called "overlays"
# Each folder in the highest hierachy is devoted to some grand meta topic
# We are only interested in the "War in Ukraine" high-level folder
#
# The "War in Ukraine" folder has one child folder for each day,
# named e.g. "20220830"
#
# Each "daily" child folder has sub-folders for each topic that occurred on
# that day:
# - Shellings
# - FIRMS Data
# - Order of battle (RU/UA)
# - Front lines
# etc.
#
# Those sub-folders for each topic then contain "Points" with geo
# coordinates and some metadata, most often just "title" and some icons

# TODO: Merge data with "archived" map with older entries
# https://www.scribblemaps.com/maps/view/Operational%20Map%20Ukraine%20(copy)/19bUdxmFGh
# https://www.scribblemaps.com/api/maps/19bUdxmFGh/smjson?cb=1665511749093


class DefmonExtractor():
    @staticmethod
    def extract_events(data, eventtype: str = 'Shellings') -> List[Event]:
        overlays = data.get('overlays')

        war_in_ukraine = list(filter(
            lambda x: x.get('id') == WAR_IN_UKRAINE_ID,
            overlays
        ))[0]

        # E.g. [ {"name": "20220815", "overlays": [...]}, ]
        days = war_in_ukraine.get('overlays')
        events = []

        DATE_INPUT_FORMAT = '%Y%m%d'

        def format_event(date: str, event: dict[str, Any]) -> Event:
            date_parsed = datetime.strptime(date, DATE_INPUT_FORMAT)
            coordinates = event.get('points')[0]
            return Event(
                id=event.get('id'),
                date=date_parsed,
                latitude=float(coordinates[0]),
                longitude=float(coordinates[1]),
                # 'title' field is the place name most of the time
                place_desc=event.get('title'),
                title=None,
                description=None,
                links=[],
                source=SOURCE_NAMES.DEFMON,
            )

        def is_relevant_aspect(overlay: dict, eventtype: str) -> bool:
            # Use 'x in y' to match partial strings
            return (overlay.get('name') or '').startswith(eventtype)

        for day in days:
            # 'aspect' is e.g. 'Shellings', 'FIRMS Data'
            for aspect in day.get('overlays'):
                if is_relevant_aspect(aspect, eventtype):
                    # 'item' would be individual points/paths/polygons
                    for item in aspect.get('overlays'):
                        events.append(format_event(day.get('name'), item))

        return events
