import json
import sys
from datetime import datetime

FPS = 25  # Frames pro Sekunde

if len(sys.argv) < 2:
    print("Usage: python3 time_difference.py <filename.json>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r") as f:
    data = json.load(f)

taskdata = data["taskData"]

start_str = taskdata["startTimeWatching"]
end_str = taskdata["endTimeWatching"]

start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ")
end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S.%fZ")

diff = end - start

# Umwandlung in hh:mm:ss:ff
total_seconds = int(diff.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
frames = int((diff.total_seconds() - total_seconds) * FPS)

time_watching = f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

print("timeWatching:", time_watching)
