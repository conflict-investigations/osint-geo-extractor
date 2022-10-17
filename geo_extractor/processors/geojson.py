import json
from typing import List, Optional

from ..dataformats import (
    Event,
    Feature,
    FeatureCollection,
    FeatureProperties,
    Geometry,
)

def format_feature(f: Event) -> Feature:
    return Feature(
        id=f.id,
        geometry=Geometry(
            # GeoJSON swaps lat/lng
            coordinates=(f.longitude, f.latitude),
        ),
        properties=FeatureProperties(
            title=f.title,
            date=(f.date.strftime('%Y-%m-%d') if f.date else None),
            description=f.description,
            links=f.links,
            source=f.source,
        ),
    )

def format_as_featurecollection(data: List[Event]) -> FeatureCollection:
    return FeatureCollection(
        features=tuple(map(format_feature, data)),
    )

def format_as_geojson(data: List[Event], indent: Optional[int] = None) -> str:
    features = format_as_featurecollection(data).features
    formatted = []
    for f in features:
        formatted.append(f.__dict__)
        # formatted.append(dict(
        #     type=f.type,
        #     id=f.id,
        #     geometry=dict(
        #         type='Point',
        #         coordinates=(
        #             f.geometry.coordinates[0],
        #             f.geometry.coordinates[1]
        #         ),
        #     ),
        #     properties=dict(
        #         title=f.properties.title,
        #         date=f.properties.date,
        #         description=f.properties.description,
        #         links=f.properties.links,
        #         source=f.properties.source,
        #     ),
        # ))
    return json.dumps(dict(
        type='FeatureCollection',
        features=formatted
    ), indent=indent)
