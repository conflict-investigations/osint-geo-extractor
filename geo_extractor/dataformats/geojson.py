from dataclasses import asdict, dataclass, field
from typing import Any, List, Optional

@dataclass
class Geometry():
    type: str = 'Point'
    # [lng, lat] because GeoJSON swaps coords
    coordinates: List[float] = field(default_factory=list)

    @property
    def __dict__(self) -> Any:
        return asdict(self)

@dataclass
class FeatureProperties():
    title: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    links: List[str] = field(default_factory=list)
    source: Optional[str] = None

    @property
    def __dict__(self) -> Any:
        return asdict(self)

@dataclass
class Feature():
    type: str = 'Feature'
    id: str = None
    geometry: Geometry = field(default_factory=Geometry)
    properties: FeatureProperties = field(default_factory=FeatureProperties)

    @property
    def __dict__(self) -> Any:
        return asdict(self)

@dataclass
class FeatureCollection():
    type: str = 'FeatureCollection'
    features: List['Feature'] = field(default_factory=list)

    @property
    def __dict__(self) -> Any:
        return asdict(self)
