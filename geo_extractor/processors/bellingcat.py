from datetime import datetime

from ..dataformats import Event

class BellingcatProcessor():
    @staticmethod
    def extract_events(data, eventtype=None):
        DATE_INPUT_FORMAT = '%m/%d/%Y'
        events = []
        # Only task is to convert JSON strings to datetime objects
        for event in data:
            e = Event(**event)
            e.date = datetime.strptime(e.date, DATE_INPUT_FORMAT)
            e.latitude = float(e.latitude)
            e.longitude = float(e.longitude)
            events.append(e)
        return events
