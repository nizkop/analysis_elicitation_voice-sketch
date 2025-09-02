import sys
from datetime import datetime, timedelta


if len(sys.argv) < 3:
    print("Verwendung: python duration_add.py <Startzeit_ISO> <Dauer_hh:mm:ss:ff> [Frames pro Sekunde]")
    sys.exit(1)

start_time_str = sys.argv[1]
duration_str = sys.argv[2]
frames_per_second = 0

# read start time (1st parameter):
start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
h, m, s, milliseconds = map(int, duration_str.split(':'))
duration = timedelta(
    hours=h,
    minutes=m,
    seconds=s,
    milliseconds=milliseconds
)

result = start_time + duration
print(result.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + 'Z')

