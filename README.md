Script that fetches bike ride activities from Strava API and prints out summary.  
Configurable date restrictions set in .env file.

#### Setup

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

#### Run
- `python3 ActivitiesParser.py`

### API Ref
https://developers.strava.com/  
https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities
