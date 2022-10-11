from dataclasses import asdict, dataclass
from typing import List

@dataclass
class Geometry():
    # [lng, lat] because GeoJSON swaps coords
    coordinates: List[float]
    type: str = 'Point'

    @property
    def __dict__(self):
        return asdict(self)

@dataclass
class FeatureProperties():
    title: str
    date: str
    description: str

    @property
    def __dict__(self):
        return asdict(self)

@dataclass
class Feature():
    id: str
    geometry: Geometry
    properties: FeatureProperties
    type: str = 'Feature'

    @property
    def __dict__(self):
        return asdict(self)

@dataclass
class FeatureCollection():
    features: List['Feature']
    type: str = 'FeatureCollection'

    @property
    def __dict__(self):
        return asdict(self)
