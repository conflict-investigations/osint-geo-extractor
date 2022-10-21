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

EXTRACTORS = {
    SOURCE_NAMES.BELLINGCAT:   BellingcatExtractor,
    SOURCE_NAMES.CENINFORES:   CenInfoResExtractor,
    SOURCE_NAMES.DEFMON:       DefmonExtractor,
    SOURCE_NAMES.GEOCONFIRMED: GeoConfirmedExtractor,
    SOURCE_NAMES.TEXTY:        TextyExtractor,
}

DOWNLOADERS = {
    SOURCE_NAMES.BELLINGCAT:   BellingcatDownloader,
    SOURCE_NAMES.CENINFORES:   CenInfoResDownloader,
    SOURCE_NAMES.DEFMON:       DefmonDownloader,
    SOURCE_NAMES.GEOCONFIRMED: GeoConfirmedDownloader,
    SOURCE_NAMES.TEXTY:        TextyDownloader,
}

GET_FUNCS = {
    SOURCE_NAMES.BELLINGCAT:   get_bellingcat_data,
    SOURCE_NAMES.CENINFORES:   get_ceninfores_data,
    SOURCE_NAMES.DEFMON:       get_defmon_data,
    SOURCE_NAMES.GEOCONFIRMED: get_geoconfirmed_data,
    SOURCE_NAMES.TEXTY:        get_texty_data,
}
