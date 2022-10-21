# geo_extractor

Library to extract geo-related information from databases such as
[Bellingcat](https://ukraine.bellingcat.com/),
[Cen4InfoRes](https://maphub.net/Cen4infoRes/russian-ukraine-monitor),
[DefMon3](https://www.scribblemaps.com/maps/view/2022051301800/nBT8ffpeGH),
[GeoConfirmed](https://geoconfirmed.azurewebsites.net/)
and
[Texty.org.ua](https://texty.org.ua/projects/107577/under-attack-what-and-when-russia-shelled-ukraine/).

## Installation
Install from [PyPI](https://pypi.org/project/osint-geo-extractor/):
```
pip install osint-geo-extractor
```

## Usage

```python
from geo_extractor import get_bellingcat_data
events = get_bellingcat_data()
for e in events[:10]:
    print(f"{e.id}: [{e.latitude}, {e.longitude}]")
```

See also the `examples/` folder.

## Docs

Convenience functions:

- `get_bellingcat_data`
- `get_ceninfores_data`
- `get_defmon_data`
- `get_geoconfirmed_data`
- `get_texty_data`

Data is returned as a list of `Event` objects:

Field            | Type
---------------- | ----
id               | str
date             | datetime
latitude         | float
longitude        | float
place_desc       | str
title            | str
description      | str
source           | str
links            | List[str]

Data formats: See `dataformats/`

Exporting to **GeoJSON**: Use `extractors.format_as_geojson(data)`

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "CIV0001",
      "geometry": {
        "type": "Point",
        "coordinates": [
          36.659031,
          49.85005
        ]
      },
      "properties": {
        "title": "<title>",
        "date": "2022-02-24",
        "description": "<desc>",
        "links": [
          "https://twitter.com/Michael1Sheldon/status/1496717647089651716",
          "https://twitter.com/AFP/status/1496768532448788482"
        ],
        "source": "BELLINGCAT"
      }
    }
  ]
}
```

## Tests

To obtain necessary testing data not shipped with the repository, install the
package into your `virtualenv` via `pip install -e .`, navigate to
`geo_extractor/tests` and run `python generate_fixtures.py`.

The tests can be run via `pytest`:

```
$ pip install pytest
$ PYTHONPATH=. pytest
```

To run a single test, use `pytest -k <test name>`.

## License
MIT
