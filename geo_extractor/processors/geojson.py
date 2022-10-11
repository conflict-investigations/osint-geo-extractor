import json

from ..dataformats import (
    Feature,
    FeatureCollection,
    FeatureProperties,
    Geometry,
)

def format_feature(f):
    return Feature(
        id=f.id,
        geometry=Geometry(
            # GeoJSON swaps lat/lng
            coordinates=(f.longitude, f.latitude),
        ),
        properties=FeatureProperties(
            title=f.title,
            date=f.date,
            description=f.description,
        ),
    )

def format_as_featurecollection(data):
    return FeatureCollection(
        features=list(map(format_feature, data)),
    )

def format_as_geojson(data):
    features = format_as_featurecollection(data).features
    formatted = []
    for f in features:
        formatted.append(dict(
            type=f.type,
            id=f.id,
            geometry=dict(
                type='Point',
                coordinates=(
                    f.geometry.coordinates[0],
                    f.geometry.coordinates[1]
                ),
            ),
            properties=dict(
                title=f.properties.title,
                date=f.properties.date.strftime("%Y-%m-%d"),
                description=f.properties.description,
            ),
        ))
    return json.dumps(dict(
        type='FeatureCollection',
        features=formatted
    ))
