import csv
import json
import os
from datetime import date, datetime
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from stravalib.client import Client

TOKENS_FILE = "tokens.json"
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


def auth():
    if os.path.isfile(TOKENS_FILE):
        print("✅ Tokens file exists. Continuing to script...")
        return

    load_dotenv()
    cid, secret = os.getenv("STRAVA_CLIENT_ID"), os.getenv("STRAVA_CLIENT_SECRET")

    if not cid or not secret:
        raise ValueError("Missing Strava credentials in environment variables.")

    client = Client()
    auth_url = client.authorization_url(
        client_id=cid, redirect_uri="http://127.0.0.1:5000/authorization"
    )

    print(f"1️⃣  Visit this URL:\n{auth_url}")

    while True:
        try:
            redirect_url = input("2️⃣  Paste the redirect URL: ").strip()
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
            "1️⃣ What day of Jan 2026 would you like to start from? (number 1-31) "
        )

    today = date.today()
    y = today.year
    after = datetime(y, 1, int(start_day), tzinfo=ZoneInfo("US/Eastern"))
    activities = client.get_activities(after=after, limit=1000)

    return activities


def save_data(data):
    rows = []
    count = 0

    for activity in data:
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

    csv_filename = "export.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Wrote {count} activities to {csv_filename}")


def main():
    auth()
    data = get_data()
    save_data(data)


if __name__ == "__main__":
    main()
