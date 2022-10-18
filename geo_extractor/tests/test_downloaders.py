from geo_extractor.downloaders import (
    BellingcatDownloader,
    CenInfoResDownloader,
    DefmonDownloader,
    GeoConfirmedDownloader,
)

# XXX: Running this requires an active internet connection
#      Downloading will take ~25Mb

def test_defmon_downloader():
    d = DefmonDownloader()
    data = d.download()
    assert 'meta' in data

def test_bellingcat_downloader():
    d = BellingcatDownloader()
    data = d.download()
    assert data[0]['id'] == 'CIV0001'

def test_ceninfores_downloader():
    d = CenInfoResDownloader()
    data = d.download()
    assert data['geojson']['type'] == 'FeatureCollection'

def test_geoconfirmed_downloader():
    d = GeoConfirmedDownloader()
    data = d.download()
    # "name": "C. Last 7 days",
    assert data['mapDataFolders'][2]['name'].startswith('C.')
