import csv
import json
import os
from datetime import date, datetime
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from stravalib import unit_helper
from stravalib.client import Client

TOKENS_FILE = "tokens.json"
CSV_FILE = "export.csv"
BRRR_CSV_HEADERS = [
    "Activity Date",
    "Elevation Gain",
    "Activity Time",
    "Activity Type",
    "Comment",
    "Distance in Miles",
]
INCOMPATIBLE = [
    "Crossfit",
    "Elliptical",
    "Golf",
    "Hike",
    "IceSkate",
    "InlineSkate",
    "Kayaking",
    "Kitesurf",
    "RockClimbing",
    "Sail",
    "Skateboard",
    "Snowshoe",
    "Surfing",
    "WeightTraining",
    "Windsurf",
    "Workout",
    "Yoga",
]
BRRR_TO_STRAVA = {
    "Run": [
        "Run",
        "Soccer",
        "VirtualRun",
    ],
    "Walk": [
        "StairStepper",
        "Walk",
    ],
    "Ride": [
        "EBikeRide",
        "Handcycle",
        "Ride",
        "Velomobile",
        "VirtualRide",
        "Wheelchair",
    ],
    "Swim": [
        "Swim",
    ],
    "Ski": [
        "AlpineSki",
        "BackcountrySki",
        "NordicSki",
        "RollerSki",
        "Snowboard",
    ],
    "Paddle/Row": [
        "Canoeing",
        "Rowing",
        "StandUpPaddling",
    ],
}


def format_time(total_seconds):
    """Formats a timedelta object into hh:mm:ss or mm:ss."""
    total_seconds = int(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"


def auth():
    if os.path.isfile(TOKENS_FILE):
        print("✅ Tokens file exists. Continuing to script...")
        return

    load_dotenv()
    cid, secret = os.getenv("STRAVA_CLIENT_ID"), os.getenv("STRAVA_CLIENT_SECRET")

    if not cid or not secret:
        raise ValueError("Missing Strava credentials in environment variables.")

    cid = int(cid)

    client = Client()
    auth_url = client.authorization_url(
        client_id=cid, redirect_uri="http://127.0.0.1:5000/authorization"
    )

    print(f"1️⃣  Visit this UL:\n{auth_url}")
    print("  Don't worry about the 404, just copy the URL it tries to redirect you to")

    while True:
        try:
            redirect_url = input("2️⃣ Paste the redirect URL: ").strip()
            code = parse_qs(urlparse(redirect_url).query)["code"][0]

            tokens = client.exchange_code_for_token(
                client_id=cid, client_secret=secret, code=code
            )

            with open(TOKENS_FILE, "w") as f:
                json.dump(tokens, f, indent=4)
            break
        except (KeyError, IndexError):
            print("❌ Invalid URL. Could not find 'code' parameter. Try again.")
        except Exception as e:
            print(f"❌ An error occurred: {e}. Try again.")

    print("✅ Successfully saved tokens. Continuing to script...")


def get_data():
    load_dotenv()
    with open(TOKENS_FILE, "r") as f:
        tokens = json.load(f)

    client = Client(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_expires=tokens["expires_at"],
    )

    start_day = "0"
    while not start_day.isnumeric() or int(start_day) < 1 or int(start_day) > 31:
        start_day = input(
            "1️⃣ What day of January would you like to start from? (number 1-31) "
        )

    today = date.today()
    y = today.year
    after = datetime(y, 1, int(start_day), tzinfo=ZoneInfo("US/Eastern"))
    activities = client.get_activities(after=after, limit=1000)

    return activities


def coerce_activity_type(activity_type) -> str | None:
    # skip activities that can't really be included in Backyard Brrr
    if activity_type in INCOMPATIBLE:
        return None

    for brrr_type, strava_types in BRRR_TO_STRAVA.items():
        if activity_type in strava_types:
            return brrr_type
    return None


def save_data(activities):
    rows = []

    for a in activities:
        activity_type = coerce_activity_type(a.sport_type)
        if activity_type is None:
            continue

        brrr_activity = {
            "Activity Date": a.start_date_local.strftime("%Y-%m-%d"),
            "Elevation Gain": f"{round(unit_helper.feet(a.total_elevation_gain).magnitude, 2)} ft",
            "Activity Time": format_time(a.moving_time),
            "Activity Type": activity_type,
            "Comment": "outside",
            "Distance in Miles": f"{round(unit_helper.miles(a.distance).magnitude, 2)} miles",
        }
        rows.append(brrr_activity)

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BRRR_CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Wrote activities to {CSV_FILE}")


def main():
    auth()
    data = get_data()
    save_data(data)


if __name__ == "__main__":
    main()
