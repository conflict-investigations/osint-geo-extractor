import csv
import io
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, List, Optional

from .base import Downloader
from ..constants import FALLBACK_DATE

TEXTY_CSV_ENDPOINT = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSyFuA7nxANnn7BwXn7az5D5L-V7yKnETgTybfKSIGmoYz2qVkc6FWSH7f0l-1Gt_dML1VpywPUzXwp/pub?gid=1376631421&single=true&output=csv'  # noqa

@dataclass
class TextyEvent():
    title: Optional[str]
    latitude: float
    longitude: float
    date: datetime
    place: Optional[str]
    coordinates_accurate: bool
    civilian_objects: bool
    link: Optional[str]
    address: Optional[str]
    projectile_type: Optional[str]
    oblast: Optional[str]
    artillery_mortars_tanks: bool
    air: bool
    missile: bool
    number_of_missiles: int

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
        data = self.request_url(TEXTY_CSV_ENDPOINT)
        return data

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
            title=row[0] or None,
            latitude=coords[0],
            longitude=coords[1],
            date=_date(row[3]),
            place=row[4] or None,
            coordinates_accurate=_coords_accurate(row[5]),
            civilian_objects=bool(row[6]),
            link=row[7] or None,
            address=row[8] or None,
            projectile_type=row[9] or None,
            oblast=row[10] or None,
            artillery_mortars_tanks=bool(row[11]),
            air=bool(row[12]),
            missile=bool(row[13]),
            number_of_missiles=_numer_of_missiles(row[14]),
        )

    def download(self) -> List[TextyEvent]:
        data = self._download()
        proxy = io.StringIO(data)  # Emulate real file to be read line by line
        next(proxy)  # Skip first row
        csv_reader = csv.reader(proxy, delimiter=',')

        events = filter(None, (self._mangle(line) for line in csv_reader))
        return [event.__dict__ for event in events]
