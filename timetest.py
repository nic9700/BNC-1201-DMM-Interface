import pytz
import time
from datetime import datetime

timestamp = datetime.now().astimezone(pytz.utc)
timestampiso = timestamp.isoformat()

print(f"Current UTC time: {timestampiso}")
print(f"Current unformatted UTC time: {timestamp}")