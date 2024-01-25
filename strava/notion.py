# from notion.block import CollectionViewBlock, PageBlock
# from notion.client import NotionClient
# from table_schema import SCHEMA

from datetime import datetime, timezone
from config import NOTION_TOKEN, DATABASE_ID, NOTION_API_BASE_URL, NOTION_API_VERSION
import requests

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

    def create_database_page_entry(self, database_id, data: dict):
        pages_url = f"{self.base_url}/pages"
        # Build the payload which in this case is a database entry
        payload = {"parent": {"database_id": database_id}, "properties": data}
    
        response = requests.post(pages_url, headers=self.headers, json=payload)
        print(f"{response.status_code}: {response.text}".split(','))
        return response
    


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
    n.create_database_page_entry(DATABASE_ID, data)

# protect against automatically running if imported
if __name__ == '__main__':
    main()
