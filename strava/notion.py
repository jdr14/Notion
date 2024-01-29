from datetime import datetime, timezone
from config import NOTION_TOKEN, DATABASE_ID, NOTION_API_BASE_URL, NOTION_API_VERSION
import requests

VERBOSE = False

class WorkoutData:
    def __init__(self, date, title, workout_type, distance, time_elapsed, calories, avg_speed, avg_power, elevation_gain):
        self.date = date
        self.title = title
        self.workout_type = workout_type
        self.distance = distance
        self.time_elapsed = time_elapsed
        self.calories = calories
        self.avg_speed = avg_speed
        self.avg_power = avg_power
        self.elevation_gain = elevation_gain

class NotionClient:
    def __init__(self, token, version, base_url):
        self.token = token
        self.version = version
        self.base_url = base_url
        self.headers = {
            "Authorization":   "Bearer " + self.token,
            "Content-Type":    "application/json",
            "Notion-Version":  self.version,
        }

    def _get_response(self, url, payload, verbose):
        response = requests.post(url, headers=self.headers, json=payload)
        if verbose:
            print(f"{response.status_code}: {response.text}".split(','))
        else:
            if response.status_code == 200:
                print(f"Response code: {response.status_code} SUCCESS!")
            else:
                print(f"Response code: {response.status_code} FAILURE!")
        return response

    def create_database_page_entry(self, database_id, data: WorkoutData):
        pages_url = f"{self.base_url}/pages"
        # Build the payload which in this case is a database entry
        payload = {
            "parent": {"database_id": database_id}, 
            "properties": {
                "Completed": { "date": {"start": data.date.isoformat(), "end": None}},
                "Workout": { "title": [ {"text": {"content": data.title} } ] },
                "Workout Type": { "select": {"name": data.workout_type } },
                "Distance": { "number": data.distance },
                "Time Elapsed": { "number": data.time_elapsed },
                "Calories": { "number": data.calories },
                "Avg Speed": { "number": data.avg_speed },
                "Avg Power": { "number": data.avg_power },
                "Elevation Gain": { "number": data.elevation_gain }
            } # End properties
        }
        return self._get_response(pages_url, payload, VERBOSE)
    
    def search_pages(self, query="", _filter=""):
        """
        Searches all pages associated with the notion connection
        """
        search_url = f"{self.base_url}/search"
        payload = {
            "query": query,
            "filter": {
                "value": _filter,
                "property": "object"
            },
            # "sort": {
            #   "direction":"ascending",
            #   "timestamp":"last_edited_time"
            # }
        }
        return self._get_response(search_url, payload, VERBOSE)

    def create_database(self, parent_id: str, db_title: str):
        """
        Creates a new database page
        """
        db_url = f"{self.base_url}/databases/"
        payload = {
           "parent": {
               "type": "page_id",
               # This is the parent notion page id to parse this, use the search_pages and look at the corresponding response json key
               "page_id": parent_id,
            }, # end parent page id
            "title": [ {
                "type": "text",
                "text": {"content": db_title}
            } ], # end title
            "properties": {
                "Completed": { 
                    "date": {} 
                },
                "Workout": { 
                    "title": {}
                },
                "Workout Type": { 
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "Run",            "color": "green"},
                            {"name": "Walk",           "color": "yellow"},
                            {"name": "Swim",           "color": "blue"},
                            {"name": "Cycling",        "color": "red"},
                            {"name": "Yoga",           "color": "pink"},
                            {"name": "Other",          "color": "gray"},
                            {"name": "StairStepper",   "color": "purple"},
                            {"name": "WeightTraining", "color": "brown"},
                        ]
                    }, # end multi select options
                },
                "Distance": { "number": {}},
                "Time Elapsed": { "number": {}},
                "Calories": { "number": {} },
                "Avg Speed": { "number": {} },
                "Avg Power": { "number": {} },
                "Elevation Gain": { "number": {} }
            } # End properties
        }

        return self._get_response(db_url, payload, VERBOSE)

def main():
    # Mainly using this for testing purposes
    title = "Test Title"
    description = "Test Description"
    published_date = datetime.now().astimezone(timezone.utc).isoformat()
    data = {
        "URL": {"title": [{"text": {"content": description}}]},
        "Title": {"rich_text": [{"text": {"content": title}}]},
        "Published": {"date": {"start": published_date, "end": None}}
    }
    n = NotionClient(NOTION_TOKEN, NOTION_API_VERSION, NOTION_API_BASE_URL)
    # n.create_database_page_entry(DATABASE_ID, data)
    # n.search_pages()

# protect against automatically running if imported
if __name__ == '__main__':
    main()
