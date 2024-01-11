import csv
import io
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, List, Optional

from .base import Downloader
from ..constants import FALLBACK_DATE

ENCODING = 'utf-8'
TEXTY_CSV_ENDPOINT = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSyFuA7nxANnn7BwXn7az5D5L-V7yKnETgTybfKSIGmoYz2qVkc6FWSH7f0l-1Gt_dML1VpywPUzXwp/pub?gid=1376631421&single=true&output=csv'  # noqa

@dataclass
class TextyEvent():
    title: Optional[str]
    latitude: float
    longitude: float
    date: datetime
    place_name: Optional[str]
    place_type: Optional[str]
    coordinates_accurate: bool
    civilian_objects: bool
    link: Optional[str]
    oblast: Optional[str]
    artillery_mortars_tanks: bool
    air: bool
    missile: bool
    number_of_missiles: int
    kamikaze_drones: bool
    projectile_type: Optional[str]
    address: Optional[str]

    @property
    def __dict__(self) -> Any:  # type: ignore
        conv = asdict(self)
        if conv['date']:
            conv['date'] = datetime.strftime(conv['date'], '%Y-%m-%d')
        return conv

class TextyDownloader(Downloader):
    """
    texty.org.ua
    Data from
    https://texty.org.ua/projects/107577/under-attack-what-and-when-russia-shelled-ukraine/
    with blessing from project authors, provided credit is given
    """  # noqa

    def _download(self) -> str:
        return self.request_url(TEXTY_CSV_ENDPOINT).read().decode(ENCODING)

    @staticmethod
    def _mangle(row: list) -> Optional[TextyEvent]:

        def _coords_accurate(statement: str) -> bool:
            if statement.lower() == 'точні':
                return True
            return False  # 'неточні' or nothing

        def _coords(row: list) -> list[float]:
            # Sometimes coordinates are given as quoted string in only
            # "latitude" row or only latitude is given with longitude missing
            try:
                return [float(row[1]), float(row[2])]
            except ValueError:
                try:
                    lat, lng = row[1].split(',')
                    return [float(lat), float(lng)]
                # Missing longitude
                except ValueError:
                    return [0.0, 0.0]

        DATE_INPUT_FORMAT_UNDERSCORES = '%Y-%m-%d'
        DATE_INPUT_FORMAT_SLASHES = '%d/%m/%Y'

        def _date(date_string: str) -> datetime:
            if not date_string:
                return FALLBACK_DATE
            try:
                return datetime.strptime(
                    date_string, DATE_INPUT_FORMAT_UNDERSCORES)
            except ValueError:
                try:
                    return datetime.strptime(
                        date_string, DATE_INPUT_FORMAT_SLASHES)
                except ValueError:
                    return FALLBACK_DATE

        def _numer_of_missiles(missile_string: str) -> int:
            try:
                return int(missile_string)
            except ValueError:
                return 0

        # This is a geo-focussed library, thus we need to weed out entries with
        # insufficient geo data
        if not (coords := _coords(row)):
            return None

        return TextyEvent(
            title=row[0] or None,  # not really a title, more of an area
            latitude=coords[0],
            longitude=coords[1],
            date=_date(row[3]),
            place_name=row[4] or None,
            place_type=row[5] or None,
            coordinates_accurate=_coords_accurate(row[6]),
            civilian_objects=bool(row[7]),
            link=row[8] or None,
            oblast=row[9] or None,
            artillery_mortars_tanks=bool(row[10]),
            air=bool(row[11]),
            missile=bool(row[12]),
            number_of_missiles=_numer_of_missiles(row[13]),
            kamikaze_drones=bool(row[14]),
            projectile_type=row[15] or None,
            address=row[16] or None,
        )

    def download(self) -> List[TextyEvent]:
        data = self._download()
        proxy = io.StringIO(data)  # Emulate real file to be read line by line
        next(proxy)  # Skip first row
        csv_reader = csv.reader(proxy, delimiter=',')

        events = filter(None, (self._mangle(line) for line in csv_reader))
        return [event.__dict__ for event in events]
