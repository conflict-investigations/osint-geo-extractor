import json
import os

from geo_extractor.downloaders import (
    BellingcatDownloader,
    CenInfoResDownloader,
    DefmonDownloader,
    GeoConfirmedDownloader,
)
from geo_extractor.constants import RAW_DATA_FILENAMES

TEST_DATA_FOLDER = 'test_data'
TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    TEST_DATA_FOLDER
)

def dump(data, filename):
    with open(os.path.join(TEST_DATA_PATH, filename), 'w') as f:
        json.dump(data, f, ensure_ascii=False)


if not os.path.isdir(TEST_DATA_PATH):
    os.mkdir(TEST_DATA_PATH)

print("Downloading Bellingcat data")
bd = BellingcatDownloader()
b_data = bd.download()
dump(b_data, RAW_DATA_FILENAMES.BELLINGCAT)

print("Downloading Cen4InfoRes data")
cd = CenInfoResDownloader()
c_data = cd.download()
dump(c_data, RAW_DATA_FILENAMES.CENINFORES)

print("Downloading Defmon data")
dd = DefmonDownloader()
d_data = dd.download()
dump(d_data, RAW_DATA_FILENAMES.DEFMON)

print("Downloading GeoConfirmed data")
gd = GeoConfirmedDownloader()
g_data = gd.download()
dump(g_data, RAW_DATA_FILENAMES.GEOCONFIRMED)
