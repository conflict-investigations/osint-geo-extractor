import json
from dataclasses import asdict, dataclass, field
from typing import Any, List, Optional

from .base import Downloader

# New unified endpoint:
BELLINGCAT_ENDPOINT = 'https://bellingcat-embeds.ams3.cdn.digitaloceanspaces.com/production/ukr/timemap/api.json'  # noqa

# Old endpoints:
BELLINGCAT_BASE = 'https://bellingcat-embeds.ams3.cdn.digitaloceanspaces.com/production/ukr'
EVENTS_ENDPOINT = BELLINGCAT_BASE + '/timemap/events.json'
SOURCES_ENDPOINT = BELLINGCAT_BASE + '/timemap/sources.json'
ASSOCIATIONS_ENDPOINT = BELLINGCAT_BASE + '/timemap/associations.json'

ENCODING = 'utf-8'

@dataclass
class BellingcatEvent():
    id: Optional[str]
    date: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    place_desc: Optional[str]
    description: Optional[str]
    sources: List['Source'] = field(default_factory=list)
    # Filters only relevant for Bellingcat entries
    filters: List['Association'] = field(default_factory=list)

    # https://www.delftstack.com/howto/python/dataclass-to-json-in-python/
    @property
    def __dict__(self) -> dict:  # type: ignore
        return asdict(self)

@dataclass
class Source():
    path: str
    id: str
    description: str

# Associations only relevant for Bellingcat entries
@dataclass
class Association():
    key: str
    value: str

class BellingcatDownloader(Downloader):
    """
    Format data as it would appear when clicking the 'export' button
    """

    def __init__(self) -> None:
        self.data = {}  # type: dict[str, Any]

    def _download(self) -> dict:
        data = {}
        data['events'] = json.loads(
                self.request_url(EVENTS_ENDPOINT).read().decode(ENCODING))
        data['sources'] = json.loads(
                self.request_url(SOURCES_ENDPOINT).read().decode(ENCODING))
        data['associations'] = json.loads(
            self.request_url(ASSOCIATIONS_ENDPOINT).read().decode(ENCODING))
        return data

    def _get_source(self, source_id: Optional[str], event_id: str
                    ) -> Optional[Source]:
        src = self.data['sources'].get(source_id)
        # Should not really happen but apparently Bellingcat's timemap
        # sometimes returns source ids for sources that do not exist (yet).
        if not src:
            return None
        return Source(id=event_id, path=src.get('paths')[0],
                      description=src.get('description'))

    def _get_association(self, association: Optional[str]
                         ) -> Optional[Association]:
        for a in self.data['associations']:
            if a.get('id') == association:
                return Association(
                    key=a['filter_paths'][0],
                    value=a['filter_paths'][1]
                )
        return None

    def _mangle(self, e: dict[str, Any]) -> BellingcatEvent:
        eventid: str = e.get('id', '')  # should always have an id tho
        return BellingcatEvent(
            id=eventid,
            date=e.get('date'),
            latitude=e.get('latitude'),
            longitude=e.get('longitude'),
            place_desc=e.get('location'),
            description=e.get('description'),
            sources=list(filter(None, (self._get_source(s, eventid)
                         for s in e.get('sources', [])))),
            filters=list(filter(None, (self._get_association(a)
                         for a in e.get('associations', [])))),
        )

    # TODO: Static method conversion? carrying instance state?
    def download(self) -> List[dict[Any, Any]]:
        self.data = self._download()
        return [self._mangle(e).__dict__ for e in self.data['events']]


"""
Reference:
https://github.com/bellingcat/ukraine-timemap/blob/590cb66a2b069fc3041662404bb0e34c896501a7/src/components/controls/DownloadButton.js#L37-L63

const exportEvents = events.map((e) => {
  return {
    id: e.civId,
    date: e.date,
    latitude: e.latitude,
    longitude: e.longitude,
    location: e.location,
    description: e.description,
    sources: e.sources.map((id) => {
      const s = sources[id];
      return {
        id,
        path: s.paths[0],
        description: s.description,
      };
    }),
    filters: e.associations.map((a) => {
      return {
        key: a.filter_paths[0],
        value: a.filter_paths[1],
      };
    }),
  };
});
return JSON.stringify(exportEvents);
"""
