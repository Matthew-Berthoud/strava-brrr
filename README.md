# Backyard Brrr Strava Activity Exporter (2026)

This repo helps you quickly import Strava activities into Backyard Brrr.
First you get set up with the Strava API to export your activities, and then you can upload them directly to Backyard Brrr!
Just follow the steps below...

## Prerequisites

- `python`: `brew install pyenv && pyenv install`
- `uv`: `brew install uv`
- Strava Account with activities that you want to upload

## Exporting Activities from Strava

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

## Uploading Activities to Backyard Brrr

1. Go to the [results page](https://runsignup.com/Race/RegistrationLookup/?raceId=103877&renderMode=results_mode), and search for yourself. ![step 1](assets/1.png)
2. Click Log Activities. ![step 2](assets/2.png)
3. Click Import Activities from CSV. ![step 3](assets/3.png)
4. Upload your generated CSV file!
