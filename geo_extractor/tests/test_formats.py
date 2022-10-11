from datetime import datetime

from geo_extractor.dataformats import Datapoint, Location, URLWithDatapoints

def test_datapoints():
    # Build example datapoint for Bellingcat database entry

    loc = Location(
        latitude=30.0,
        longitude=50.0,
        place_desc='Sumy',
    )

    d = Datapoint(
        id='CIV0001',
        date=datetime.strptime('2022-02-24', '%Y-%m-%d'),
        source='BELLINGCAT',
        description='Some event',
        location=loc,
    )

    u = URLWithDatapoints(
        url='https://foo',
        datapoints=[d],
    )

    assert u.datapoints[0].id == 'CIV0001'
