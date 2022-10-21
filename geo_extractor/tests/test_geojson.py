import json
from datetime import datetime

from geo_extractor.dataformats import Event
from geo_extractor.constants import SOURCE_NAMES
from geo_extractor.extractors import (
    format_as_geojson,
)

TEST_EVENT = Event(
    id='ABC1',
    date=datetime(2022, 2, 24),
    latitude=30.0,
    longitude=50.0,
    place_desc=None,
    title='Title',
    description='Description',
    links=['https://foo.bar'],
    source=SOURCE_NAMES.CENINFORES,
)
EXPECTED_STR_PLAIN = '{"type": "FeatureCollection", "features": [{"type": "Feature", "id": "ABC1", "geometry": {"type": "Point", "coordinates": [50.0, 30.0]}, "properties": {"title": "Title", "date": "2022-02-24", "description": "Description", "links": ["https://foo.bar"], "source": "CENINFORES"}}]}'  # noqa
EXPECTED_STR_INDENTED = """{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "ABC1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          50.0,
          30.0
        ]
      },
      "properties": {
        "title": "Title",
        "date": "2022-02-24",
        "description": "Description",
        "links": [
          "https://foo.bar"
        ],
        "source": "CENINFORES"
      }
    }
  ]
}"""

def test_geojson_plain():
    events_geojson = format_as_geojson([TEST_EVENT])
    assert events_geojson == EXPECTED_STR_PLAIN
    assert json.loads(events_geojson)['features'][0]['id'] == 'ABC1'

def test_geojson_indent():
    events_geojson = format_as_geojson([TEST_EVENT], indent=2)
    assert events_geojson == EXPECTED_STR_INDENTED
