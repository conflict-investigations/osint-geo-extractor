import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import cast, Any, Iterable, List, Optional, Union

from ..constants import FALLBACK_DATE, FALLBACK_DATE_STR, SOURCE_NAMES
from ..dataformats import Event

link_extract_regex = r"(https?://.+?)([ ,\n\\<>]|$)"
geoconfirmed_regex = r"https://twitter\.com/GeoConfirmed/status/(\d+)([ ,\n]|$)"  # noqa

@dataclass
class MapDataFolder:
    id: str = ''
    mapDataPlacemarks: List[dict[str, Union[str, List[float]]]
                            ] = field(default_factory=list)
    mapDataPolygons: List = field(default_factory=list)
    mapDataLines: List = field(default_factory=list)
    name: str = ''
    isExtended: bool = False
    # {
    #     'id': '5ae1fd70-41d4-4a71-21ca-08dabc421508',
    #     'mapDataPlacemarks': [
    #         {
    #             'id': '86c96224-077b-494b-0064-08dabc42150c',
    #             'name': 'Belarus - Vehicle Movement',
    #             'description': 'foo',
    #             'coordinates': [-68.870807, -128.823841],
    #             'icon': '_CIRCLES_BE_56_34.png'
    #         },
    #     ],
    #     'mapDataPolygons': [],
    #     'mapDataLines': [],
    #     'name': 'A. Legend - Last Map Update 20 2021 DEC',
    #     'isExtended': False,
    # },

@dataclass
class GeoConfirmedSchema:
    lastUpdate: str = ''
    mapDataFolders: List['MapDataFolder'] = field(default_factory=list)
    icons: List[str] = field(default_factory=list)
    # [
    #     '_CIRCLES_BE_56_07.png',
    # ]

    def get(self, prop: str, default: Any) -> Any:
        pass

class GeoConfirmedExtractor():
    @staticmethod
    def extract_events(data: Any) -> List[Event]:

        cast(GeoConfirmedSchema, data)

        events: List[Event] = []

        def is_relevant(folder: dict[str, Any]) -> bool:
            # Filter out metadata folders
            if folder.get('name', 'C.')[:2] in ('A.', 'B.'):
                return False
            return True

        map_data_folders: List[dict[str, Any]] = data.get('mapDataFolders', [])

        folders: Iterable[dict[str, Any]] = filter(
            is_relevant,
            map_data_folders
        )

        # Example: "2022-10-10T16:20:00"
        DATE_INPUT_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

        def parse_date(d: str) -> datetime:
            # Note: e.g. twitter.com/GeoConfirmed/status/1579567301963440128
            # has a wrong date (twitter id instead of date string)
            try:
                return datetime.strptime(d, DATE_INPUT_FORMAT)
            except ValueError:
                # Input string was invalid:
                return FALLBACK_DATE

        for folder in folders:
            placemarks: Any = folder.get('mapDataPlacemarks')
            if not placemarks:
                continue

            for item in placemarks:
                sources = []  # type: List[str]
                if (links := re.findall(link_extract_regex,
                                        item.get('description'))):
                    sources.extend((link for link, _unused in links))

                # Formerly, we used to use the tweet id as a stable key
                # But the Azure application provides UUIDs, so use them
                # instead
                # This function kept as fallback
                def get_id(desc: str) -> Optional[str]:
                    status = re.findall(geoconfirmed_regex, desc)
                    if status:
                        return status[0][0]
                    return None

                event = Event(
                    id=item.get('id', get_id(item.get('description'))),
                    date=parse_date(item.get('date', FALLBACK_DATE_STR)),
                    # Coordinates swapped
                    latitude=float(item.get('coordinates')[1]),
                    longitude=float(item.get('coordinates')[0]),
                    place_desc=None,
                    title=item.get('name'),
                    description=item.get('description'),
                    links=sources,
                    source=SOURCE_NAMES.GEOCONFIRMED,
                )
                events.append(event)

        return events
