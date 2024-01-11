import pytest
from geo_extractor.downloaders import (
    BellingcatDownloader,
    CenInfoResDownloader,
    DefmonDownloader,
    DefmonSpreadsheetDownloader,
    GeoConfirmedDownloader,
    # ReukraineDownloader,
    TextyDownloader,
)

# XXX: Running this requires an active internet connection
#      Downloading will take ~25Mb

# XXX: Currently not working correctly due to data format change
@pytest.mark.skip(reason="currently broken")
@pytest.mark.online
def test_defmon_downloader():
    d = DefmonDownloader()
    data = d.download()
    assert 'meta' in data

@pytest.mark.online
def test_defmon_spreadsheet_downloader():
    d = DefmonSpreadsheetDownloader()
    data = d.download()
    # First row of raw .csv file should be mostly empty
    assert data[:28] == ',,,,,,,,Count,37,32,24,39,6,'

@pytest.mark.online
def test_bellingcat_downloader():
    d = BellingcatDownloader()
    data = d.download()
    assert data[0]['id'] == 'Q0YLYJ'

@pytest.mark.online
def test_ceninfores_downloader():
    d = CenInfoResDownloader()
    data = d.download()
    assert data['type'] == 'FeatureCollection'
    assert data['features'][0]['properties']['id'] == 'UW0001'

@pytest.mark.skip(reason="Data format changed")
@pytest.mark.online
def test_geoconfirmed_downloader():
    d = GeoConfirmedDownloader()
    data = d.download()
    # "name": "C. Last 7 days",
    assert data['mapDataFolders'][2]['name'].startswith('C.')

# @pytest.mark.online
# def test_reukraine_downloader():
#     d = ReukraineDownloader()
#     data = d.download()
#     assert data[0]['id'] == 'CIV0001'

@pytest.mark.online
def test_texty_downloader():
    d = TextyDownloader()
    data = d.download()
    assert data[0]['title'] == 'Харків'
    assert data[0]['date'] == '2022-02-25'
