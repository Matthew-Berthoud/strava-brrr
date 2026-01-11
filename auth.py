import os

from dotenv import load_dotenv
from stravalib.client import Client

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")


def main():
    client = Client()

    url = client.authorization_url(
        client_id=CLIENT_ID,
        redirect_uri="http://127.0.0.1:5000/authorization",
    )
    print(url)

    # Paste that url into a browser, then it will attempt to redirect you
    # The url it redirects you to will contain a `code` whose value you
    # should paste below

    token_response = client.exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code="YOUR CODE HERE",
    )
    print(token_response)

    # Save that token to `token_response.json`, then run main.py


if __name__ == "__main__":
    main()
