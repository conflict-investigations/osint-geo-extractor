# Usage example: Narrowing down results from DefMon3 shellings
# Prints results on console
# Careful: Downloads ~20Mb of data from scribblemaps.com

from datetime import datetime
import math
from geo_extractor.downloaders import DefmonDownloader
from geo_extractor.extractors import DefmonExtractor

print('Downloading...')
d = DefmonDownloader()
data = d.download()

print('Finished downloading')

# Save to disk:
# import json
# from geo_extractor.constants import RAW_DATA_FILENAMES
# with open(RAW_DATA_FILENAMES.DEFMON, 'w') as f:
#     json.dump(data, f, ensure_ascii=False)

# Load from disk:
# with open(RAW_DATA_FILENAMES.DEFMON, 'r') as f:
#     data = json.load(f)

p = DefmonExtractor()
events = p.extract_events(data, 'Shellings')

# Only pick out events that match a certain lat/lng
def is_in_bounds(e):
    if math.floor(e.latitude) != 47:
        return False
    if math.floor(e.longitude) != 34:
        return False
    # Only results from Oct. 1st until Oct 11th:
    if e.date < datetime(2022, 10, 1) or e.date > datetime(2022, 10, 11):
        return False
    return True


print('\nShellings at [47.x, 34.x] between Oct. 1st and Oct. 11th:\n')

filtered = filter(is_in_bounds, events)
for event in filtered:
    print(event)
