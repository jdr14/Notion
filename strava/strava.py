from stravaio import strava_oauth2
from stravaio import StravaIO

from config import CLIENT_ID, CLIENT_SECRET
from public_config import NOTION_API_BASE_URL, NOTION_API_VERSION
from notion import NotionClient, WorkoutData

import json

# Modify this macro to the year of the data you want to start with
CURRENT_YEAR = 2024

NOTION_PAGE_NAME = "Fitness"

def main():
    # Get OAUTH token using the client ID and secret
    token = strava_oauth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Authenticate with Strava API
    client = StravaIO(access_token=token["access_token"])

    # Get Strava Data in a list called 'activities'
    activities = client.get_logged_in_athlete_activities(after=f'{CURRENT_YEAR}-01-01T00:00:00Z')

    # Create a notion client object
    notion = NotionClient(NOTION_API_VERSION, NOTION_API_BASE_URL)

    # Search the notion pages for the 32 digit uid of the parent page
    parent_id = notion.search_pages(query=NOTION_PAGE_NAME, _filter="page").json()["results"][0]["id"] 

    year = CURRENT_YEAR

    page_list = notion.get_databases_and_pages(parent_id=parent_id)
    return 

    # Create and remember the databse id
    table = notion.create_database(parent_id=parent_id, db_title=str(year))
    db_id = json.loads(table.text)["id"]

    for activity in activities:
        # Pull the year parsed from the activity data
        curr_year = int(activity.start_date_local.date().strftime("%Y"))
        if curr_year > year:
            year = curr_year # Update to the current year detected from the activity
            table = notion.create_database(parent_id=str(parent_id), db_title=str(year))
            db_id = json.loads(table.text)["id"]

        if not activity.type:
            activity.type = "Other"

        data_entry = WorkoutData(
            activity.start_date,
            activity.name,
            activity.type,
            activity.distance,
            activity.elapsed_time,
            activity.kilojoules,
            activity.average_speed,
            activity.average_watts,
            activity.total_elevation_gain,
        )
        notion.create_database_page_entry(db_id, data_entry)

if __name__ == '__main__':
    main()
