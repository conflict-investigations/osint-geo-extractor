from .constants import *  # noqa
from .dataformats import *  # noqa
from .downloaders import *  # noqa
from .processors import *  # noqa

# Convenience functions:

def get_bellingcat_data():
    data = BellingcatDownloader().download()
    return BellingcatProcessor().extract_events(data)

def get_ceninfores_data():
    data = CenInfoResDownloader().download()
    return CenInfoResProcessor().extract_events(data)

def get_defmon_data():
    data = DefmonDownloader().download()
    return DefmonProcessor().extract_events(data)

def get_geoconfirmed_data():
    data = GeoConfirmedDownloader().download()
    return GeoConfirmedProcessor().extract_events(data)
