# Strava Activity Exporter (2026)

This script fetches all your Strava activities for the year 2026 using the `stravalib` library and exports them to a CSV file.

## Prerequisites

- **uv** (Python package manager)
- **Strava Account**
- **Strava API Access Token** with `activity:read_all` permissions.

## Setup

1.  **Clone the repo:**

    ```zsh
    git clone git@github.com:Matthew-Berthoud/strava-brrr.git
    cd strava-brrr
    ```

2.  **Initialize the project:**
    If you haven't already initialized a uv project in this directory:

    ```zsh
    uv init
    ```

3.  **Add dependencies:**
    Install `stravalib` for the API and `python-dotenv` for environment variable management.

    ```zsh
    uv add stravalib python-dotenv
    ```

4.  **Configure Environment Variables:**
    Create a file named `.env` in the root directory and add your Strava token:

    ```zsh
    cp .env.example .env
    open .env
    ```

    ```ini
    STRAVA_ACCESS_TOKEN=your_actual_token_string_here
    ```

## Usage

Run the script using `uv run`:

```bash
uv run export_activities.py
```
