from dataclasses import dataclass
from datetime import datetime

ENCODING: str = 'utf-8'

FALLBACK_DATE: datetime = datetime(2022, 2, 24)
FALLBACK_DATE_STR: str = '2022-02-24'

# XXX use this more
link_extract_regex: str = r"(https?://.+?)([ ,\n\\<>]|$)"

@dataclass
class RAW_DATA_FILENAMES():
    BELLINGCAT:     str = 'bellingcat-raw.json'
    CENINFORES:     str = 'ceninfores-raw.json'
    DEFMON:         str = 'defmon-raw.json'
    DEFMON_CSV:     str = 'defmon-raw.csv'
    GEOCONFIRMED:   str = 'geoconfirmed-raw.kml'
    # REUKRAINE:      str = 'reukraine-raw.json'
    TEXTY:          str = 'texty-raw.json'

@dataclass
class SOURCE_NAMES():
    BELLINGCAT:         str = 'BELLINGCAT'
    CENINFORES:         str = 'CENINFORES'
    DEFMON:             str = 'DEFMON'
    # XXX simply remove old DefMon3 source?
    # DEFMON_SPREADSHEET: str = 'DEFMON_SPREADSHEET'
    GEOCONFIRMED:       str = 'GEOCONFIRMED'
    # REUKRAINE:          str = 'REUKRAINE'
    TEXTY:              str = 'TEXTY'
