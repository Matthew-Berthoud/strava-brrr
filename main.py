import csv
import json
from datetime import date, datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from stravalib.client import Client

METERS_TO_MILES = 0.000621371
METERS_TO_FEET = 3.28084


def format_time(total_seconds):
    """Formats a timedelta object into hh:mm:ss or mm:ss."""
    total_seconds = int(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"


with open("token_response.json", "r") as f:
    token_refresh = json.load(f)

try:
    load_dotenv()

    client = Client(
        access_token=token_refresh["access_token"],
        refresh_token=token_refresh["refresh_token"],
        token_expires=token_refresh["expires_at"],
    )
except:
    print(
        "Failed to instantiate client. Take a look at auth.py, and https://stravalib.readthedocs.io/en/latest/get-started/authenticate-with-strava.html"
    )
    exit()


start_day = "0"
while not start_day.isnumeric() or int(start_day) < 1 or int(start_day) > 31:
    start_day = input(
        "What day of Jan 2026 would you like to start from? (number 1-31) "
    )

today = date.today()
y = today.year
after = datetime(y, 1, int(start_day), tzinfo=ZoneInfo("US/Eastern"))
activities = client.get_activities(after=after, limit=1000)

rows = []
count = 0

for activity in activities:
    count += 1

    act_date = activity.start_date_local.strftime("%Y-%m-%d")
    act_time = format_time(activity.moving_time)

    if activity.total_elevation_gain is not None:
        elevation_feet = float(activity.total_elevation_gain) * METERS_TO_FEET
        elevation_str = f"{elevation_feet:.0f} ft"
    else:
        elevation_str = "0 ft"

    act_type = str(getattr(activity, "sport_type", activity.type))[6:-1]
    if act_type == "WeightTraining":
        continue
    if act_type == "AlpineSki":
        act_type = "Ski"

    comment = "outside"

    if activity.distance is not None:
        distance_miles = float(activity.distance) * METERS_TO_MILES
        distance_str = f"{distance_miles:.2f}"
    else:
        distance_str = "0.00"

    rows.append(
        {
            "Activity Date": act_date,
            "Elevation Gain": elevation_str,
            "Activity Time": act_time,
            "Activity Type": act_type,
            "Comment": comment,
            "Distance in Miles": distance_str,
        }
    )

headers = [
    "Activity Date",
    "Elevation Gain",
    "Activity Time",
    "Activity Type",
    "Comment",
    "Distance in Miles",
]


csv_filename = "backyard_brrr_strava_export.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"Success! Wrote {count} activities to {csv_filename}")
