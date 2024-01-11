import json
import pytest
from geo_extractor.extractors import (
    BellingcatExtractor,
    CenInfoResExtractor,
    DefmonExtractor,
    DefmonSpreadsheetExtractor,
    GeoConfirmedExtractor,
    # ReukraineExtractor,
    TextyExtractor,
    format_as_geojson
)

from .fixtures import (  # noqa
    bellingcat_raw,
    ceninfores_raw,
    defmon_raw,
    defmon_spreadsheet_raw,
    geoconfirmed_raw,
    # reukraine_raw,
    texty_raw,
)

def test_bellingcat_extractor_extract(bellingcat_raw):  # noqa
    b_extractor = BellingcatExtractor()

    events = b_extractor.extract_events(bellingcat_raw)

    # TODO: Temporary checking if empty lat/lng values are included
    outlier = [e for e in events if e.id == 'EHIWGJ'][0]
    assert outlier.latitude == 0.0

    assert events[-1].id == 'CIV0003'

def test_bellingcat_geojson(bellingcat_raw):  # noqa
    b_extractor = BellingcatExtractor()

    events = b_extractor.extract_events(bellingcat_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(events_geojson)['features'][-1]['id'] == 'CIV0003'

def test_ceninfores_extractor_extract(ceninfores_raw):  # noqa
    c_extractor = CenInfoResExtractor()

    events = c_extractor.extract_events(ceninfores_raw)
    assert events[0].id == 'UW0001'

def test_ceninfores_geojson(ceninfores_raw):  # noqa
    c_extractor = CenInfoResExtractor()

    events = c_extractor.extract_events(ceninfores_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(events_geojson)['features'][0]['id'] == 'UW0001'

# XXX: Currently not working correctly due to data format change
@pytest.mark.skip(reason="currently broken")
def test_defmon_extractor_extract(defmon_raw):  # noqa
    d_extractor = DefmonExtractor()

    shellings_data = d_extractor.extract_events(defmon_raw, 'Shellings')
    assert shellings_data[0].id == '4cd03b2245'

    firms_data = d_extractor.extract_events(defmon_raw, 'FIRMS Data')
    assert firms_data[0].id == '8c68f57511f24377b537975898379e70'

# XXX: Currently not working correctly due to data format change
@pytest.mark.skip(reason="currently broken")
def test_defmon_geojson(defmon_raw):  # noqa
    d_extractor = DefmonExtractor()

    shellings_data = d_extractor.extract_events(defmon_raw, 'Shellings')
    shellings_geojson = format_as_geojson(shellings_data)
    assert json.loads(shellings_geojson)['features'][0]['id'] == '4cd03b2245'

    firms_data = d_extractor.extract_events(defmon_raw, 'FIRMS Data')
    firms_geojson = format_as_geojson(firms_data)
    assert json.loads(firms_geojson)['features'][0]['id'] \
        == '8c68f57511f24377b537975898379e70'

def test_defmon_spreadsheet_extractor_extract(defmon_spreadsheet_raw):  # noqa
    ds_extractor = DefmonSpreadsheetExtractor()

    shellings_data = ds_extractor.extract_events(defmon_spreadsheet_raw)
    assert shellings_data[0].date.strftime('%Y-%m-%d') == '2022-06-09'
    assert shellings_data[0].latitude == 50.382503
    assert shellings_data[0].longitude == 36.061166
    assert shellings_data[0].place_desc == 'Udy'

# XXX: Currently not working correctly due to data format change
@pytest.mark.skip(reason="currently broken")
def test_geoconfirmed_extractor_extract(geoconfirmed_raw):  # noqa
    g_extractor = GeoConfirmedExtractor()

    events = sorted(g_extractor.extract_events(geoconfirmed_raw),
                    key=lambda x: x.date)
    assert events[0].id == '5df5a8ea-952c-4dbd-2923-08db5258bd64'

# XXX: Currently not working correctly due to data format change
@pytest.mark.skip(reason="currently broken")
def test_geoconfirmed_geojson(geoconfirmed_raw):  # noqa
    g_extractor = GeoConfirmedExtractor()

    events = sorted(g_extractor.extract_events(geoconfirmed_raw),
                    key=lambda x: x.date)
    events_geojson = format_as_geojson(events)
    assert json.loads(events_geojson)['features'][0]['id'] \
        == '5df5a8ea-952c-4dbd-2923-08db5258bd64'

def test_texty_extractor_extract(texty_raw):  # noqa
    t_extractor = TextyExtractor()

    events = t_extractor.extract_events(texty_raw)
    assert events[0].place_desc == 'Харківська'

def test_texty_geojson(texty_raw):  # noqa
    t_extractor = TextyExtractor()

    events = t_extractor.extract_events(texty_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(
        events_geojson)['features'][0]['properties']['title'] == 'Харків'
