# Backyard Brrr Strava Activity Exporter

## Prerequisites

- `python`
- `uv`
- Strava Account with activities that you want to upload

## Setup

1. Clone the repo:

   ```zsh
   git clone git@github.com:Matthew-Berthoud/strava-brrr.git
   cd strava-brrr
   ```

2. Initialize the project dependencies:

   ```zsh
   uv sync
   ```

3. Set up an application in your Strava account by following the [beginning of this tutorial](https://stravalib.readthedocs.io/en/latest/get-started/authenticate-with-strava.html#step-1-create-an-application-in-your-strava-account)

4. Get your client secret and client id for this application, and put them in an `.env` file:

   ```sh
   cp .env.example .env
   # open .env and fill in fields
   ```

5. Run the script and follow all instructions:

   ```sh
   uv run main.py
   ```

6. Upload `export.csv` to the Backyard Brrr [results page](https://runsignup.com/Race/RegistrationLookup/?raceId=103877&renderMode=results_mode)

7. If you have any trouble, open an Issue or Slack message me!
