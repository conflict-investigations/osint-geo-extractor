import argparse
import json
import os

from geo_extractor.downloaders import (
    BellingcatDownloader,
    CenInfoResDownloader,
    DefmonDownloader,
    GeoConfirmedDownloader,
    # ReukraineDownloader,
    TextyDownloader,
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

def download_bellingcat():
    print("Downloading Bellingcat data")
    bd = BellingcatDownloader()
    b_data = bd.download()
    dump(b_data, RAW_DATA_FILENAMES.BELLINGCAT)

def download_ceninfores():
    print("Downloading Cen4InfoRes data")
    cd = CenInfoResDownloader()
    c_data = cd.download()
    dump(c_data, RAW_DATA_FILENAMES.CENINFORES)

def download_defmon():
    print("Downloading Defmon data")
    dd = DefmonDownloader()
    d_data = dd.download()
    dump(d_data, RAW_DATA_FILENAMES.DEFMON)

def download_geoconfirmed():
    print("Downloading GeoConfirmed data")
    gd = GeoConfirmedDownloader()
    g_data = gd.download()
    dump(g_data, RAW_DATA_FILENAMES.GEOCONFIRMED)

# def download_reukraine():
#     print("Downloading Reukraine data")
#     rd = ReukraineDownloader()
#     r_data = rd.download()
#     dump(r_data, RAW_DATA_FILENAMES.REUKRAINE)

def download_texty():
    print("Downloading Texty data")
    td = TextyDownloader()
    t_data = td.download()
    dump(t_data, RAW_DATA_FILENAMES.TEXTY)

def main():
    if not os.path.isdir(TEST_DATA_PATH):
        os.mkdir(TEST_DATA_PATH)
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', default=None,
        type=str, help='Source to download. Leave empty to download all')
    args = parser.parse_args()
    _mapping = {
        'bellingcat': download_bellingcat,
        'ceninfores': download_ceninfores,
        'defmon': download_defmon,
        'geoconfirmed': download_geoconfirmed,
        'texty': download_texty,
    }
    if not args.source:
        print('No name given, downloading all')
        download_bellingcat()
        download_ceninfores()
        download_defmon()
        download_geoconfirmed()
        download_texty()
    else:
        _mapping[args.source]()


if __name__ == '__main__':
    main()
