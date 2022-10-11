import json
from urllib import request

from .base import Downloader
from ..dataformats import Association, Event, Source

BELLINGCAT_BASE = 'https://ukraine.bellingcat.com/ukraine-server/api/ukraine'
EVENTS_ENDPOINT = BELLINGCAT_BASE + '/export_events/deeprows'
SOURCES_ENDPOINT = BELLINGCAT_BASE + '/export_sources/deepids'
ASSOCIATIONS_ENDPOINT = BELLINGCAT_BASE + '/export_associations/deeprows'

ENCODING = 'utf-8'

class BellingcatDownloader(Downloader):
    """
    Format data as it would appear when clicking the 'export' button
    """

    def __init__(self):
        self.data = {}

    @staticmethod
    def _download():
        data = {}
        data['events'] = json.loads(
            request.urlopen(EVENTS_ENDPOINT).read().decode(ENCODING))
        data['sources'] = json.loads(
            request.urlopen(SOURCES_ENDPOINT).read().decode(ENCODING))
        data['associations'] = json.loads(
            request.urlopen(ASSOCIATIONS_ENDPOINT).read().decode(ENCODING))
        return data

    def _get_source(self, source_id, event_id):
        src = self.data['sources'].get(source_id)
        return Source(id=event_id, path=src.get('paths')[0],
                    description=src.get('description'))

    def _get_association(self, association):
        assoc = list(filter(None,
            (a for a in self.data['associations']
                if a.get('id') == association)
        ))[0]
        return Association(
            key=assoc['filter_paths'][0],
            value=assoc['filter_paths'][1]
        )

    def _mangle(self, e):
        eventid = e.get('id')
        return Event(
            id=eventid,
            date=e.get('date'),
            latitude=e.get('latitude'),
            longitude=e.get('longitude'),
            place_desc=e.get('location'),
            title=None,
            description=e.get('description'),
            sources=[self._get_source(s, eventid) for s in e.get('sources')],
            filters=[self._get_association(a) for a in e.get('associations')],
        )

    def download(self):
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
