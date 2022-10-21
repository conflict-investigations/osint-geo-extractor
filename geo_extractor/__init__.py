from typing import List

from .constants import *  # noqa
from .dataformats import *  # noqa
from .downloaders import *  # noqa
from .extractors import *  # noqa

# Convenience functions:

def get_bellingcat_data() -> List[Event]:
    data = BellingcatDownloader().download()
    return BellingcatExtractor().extract_events(data)

def get_ceninfores_data() -> List[Event]:
    data = CenInfoResDownloader().download()
    return CenInfoResExtractor().extract_events(data)

def get_defmon_data(eventtype: str = 'Shellings') -> List[Event]:
    data = DefmonDownloader().download()
    return DefmonExtractor().extract_events(data, eventtype)

def get_geoconfirmed_data() -> List[Event]:
    data = GeoConfirmedDownloader().download()
    return GeoConfirmedExtractor().extract_events(data)

# def get_reukraine_data() -> List[Event]:
#     data = ReukraineDownloader().download()
#     return ReukraineExtractor().extract_events(data)

def get_texty_data() -> List[Event]:
    data = TextyDownloader().download()
    return TextyExtractor().extract_events(data)
