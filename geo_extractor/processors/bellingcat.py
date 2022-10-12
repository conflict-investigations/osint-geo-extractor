from datetime import datetime

from ..constants import SOURCE_NAMES
from ..dataformats import Event

class BellingcatProcessor():
    @staticmethod
    def extract_events(data, eventtype=None):
        DATE_INPUT_FORMAT = '%m/%d/%Y'
        events = []
        # Convert JSON strings to datetime objects, set links
        for event in data:
            links = [s['path'] for s in event.pop('sources')]
            event.pop('filters')
            e = Event(**event)
            e.date = datetime.strptime(e.date, DATE_INPUT_FORMAT)
            e.latitude = float(e.latitude)
            e.longitude = float(e.longitude)
            e.source = SOURCE_NAMES.BELLINGCAT
            e.links = links
            events.append(e)
        return events
