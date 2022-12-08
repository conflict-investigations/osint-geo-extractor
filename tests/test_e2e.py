import json
from geo_extractor.extractors import (
    BellingcatExtractor,
    CenInfoResExtractor,
    DefmonExtractor,
    GeoConfirmedExtractor,
    # ReukraineExtractor,
    TextyExtractor,
    format_as_geojson
)

from .fixtures import (  # noqa
    bellingcat_raw,
    ceninfores_raw,
    defmon_raw,
    geoconfirmed_raw,
    # reukraine_raw,
    texty_raw,
)

def test_bellingcat_extractor_extract(bellingcat_raw):  # noqa
    b_extractor = BellingcatExtractor()

    events = b_extractor.extract_events(bellingcat_raw)
    assert events[0].id == 'CIV0001'

def test_bellingcat_geojson(bellingcat_raw):  # noqa
    b_extractor = BellingcatExtractor()

    events = b_extractor.extract_events(bellingcat_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(events_geojson)['features'][0]['id'] == 'CIV0001'

def test_ceninfores_extractor_extract(ceninfores_raw):  # noqa
    c_extractor = CenInfoResExtractor()

    events = c_extractor.extract_events(ceninfores_raw)
    assert events[0].id == 'UW0001'

def test_ceninfores_geojson(ceninfores_raw):  # noqa
    c_extractor = CenInfoResExtractor()

    events = c_extractor.extract_events(ceninfores_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(events_geojson)['features'][0]['id'] == 'UW0001'

def test_defmon_extractor_extract(defmon_raw):  # noqa
    d_extractor = DefmonExtractor()

    shellings_data = d_extractor.extract_events(defmon_raw, 'Shellings')
    assert shellings_data[0].id == '4cd03b2245'

    firms_data = d_extractor.extract_events(defmon_raw, 'FIRMS Data')
    assert firms_data[0].id == '8c68f57511f24377b537975898379e70'

def test_defmon_geojson(defmon_raw):  # noqa
    d_extractor = DefmonExtractor()

    shellings_data = d_extractor.extract_events(defmon_raw, 'Shellings')
    shellings_geojson = format_as_geojson(shellings_data)
    assert json.loads(shellings_geojson)['features'][0]['id'] == '4cd03b2245'

    firms_data = d_extractor.extract_events(defmon_raw, 'FIRMS Data')
    firms_geojson = format_as_geojson(firms_data)
    assert json.loads(firms_geojson)['features'][0]['id'] \
        == '8c68f57511f24377b537975898379e70'

def test_geoconfirmed_extractor_extract(geoconfirmed_raw):  # noqa
    g_extractor = GeoConfirmedExtractor()

    events = g_extractor.extract_events(geoconfirmed_raw)
    assert events[0].id == '1582105830240837632'

def test_geoconfirmed_geojson(geoconfirmed_raw):  # noqa
    g_extractor = GeoConfirmedExtractor()

    events = g_extractor.extract_events(geoconfirmed_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(events_geojson)['features'][0]['id'] \
        == '1582105830240837632'

def test_texty_extractor_extract(texty_raw):  # noqa
    t_extractor = TextyExtractor()

    events = t_extractor.extract_events(texty_raw)
    assert events[0].title == 'Харків'

def test_texty_geojson(texty_raw):  # noqa
    t_extractor = TextyExtractor()

    events = t_extractor.extract_events(texty_raw)
    events_geojson = format_as_geojson(events)
    assert json.loads(
        events_geojson)['features'][0]['properties']['title'] == 'Харків'
