from stravaio import strava_oauth2
from stravaio import StravaIO

from config import CLIENT_ID, CLIENT_SECRET
from notion_api import NotionInterface

# Modify this macro to the year of the data you want to start with
CURRENT_YEAR = 2021 

# Get OAUTH token using the client ID and secret
token = strava_oauth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Get Strava Data in a list called 'activities'
client = StravaIO(access_token=token["access_token"])
activities = client.get_logged_in_athlete_activities(after=f'{CURRENT_YEAR}-01-01T00:00:00Z')

for activity in activities:
    curr_year = int(activity.start_date_local.date().strftime("%Y"))
    if curr_year > year:
        year = curr_year # Update to the current year detected from the activity