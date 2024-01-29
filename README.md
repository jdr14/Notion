
# Strava To Notion Bridge

The purpose of this application is to serve as a data bridge between the widely used fitness app Strava and the popular productivity app called Notion.  As of right now, it can authenticate with strava, extracta all workouts from a given year, and upload those as database entries under a user's "Fitness" Notion page. 





## Setup

First install the requirements (Optional - You can set this up in a virtual environment if you wish to do so https://docs.python.org/3/library/venv.html)

```bash
  python -m pip install -r requirements.txt
```

## Strava Setup

After installing, head over to https://developers.strava.com/docs/getting-started/ section B. You should be able to get your client id and client secret from https://www.strava.com/settings/api and create a config.py file in the strava to save the macros defined as CLIENT_ID and CLIENT_SECRET.
```bash
# Example config.py file contains
    CLIENT_ID = # your client id here 
    CLIENT_SECRET = # your client secret here
```

## Notion Setup

Head over to https://developers.notion.com/docs/create-a-notion-integration and create a notion integration.  Once you're done, you should be able to see your secret at https://www.notion.so/my-integrations/ under the "secrets" tab.  As done above, save your secret in a NOTION_TOKEN macro.

```bash
# Example config.py file continued
    NOTION_TOKEN = # your token here.
```

Now that you have a Notion integration, go to your Notion "Fitness" page and in the top right corner click the three dots ... and add your connection.  
## Running

```bash
python strava.py
```
## Authors

- [@jdr14](https://github.com/jdr14)

