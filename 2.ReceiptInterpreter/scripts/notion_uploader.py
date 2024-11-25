from notion_client import Client
import yaml

# Load configuration settings
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

notion = Client(auth=config["notion_api_key"])

def send_to_notion(recipe_data):
    """
    Uploads recipe information to a Notion database.
    """
    notion.pages.create(
        parent={"database_id": config["database_id"]},
        properties={
            "Name": {"title": [{"text": {"content": recipe_data['name']}}]},
            "Ingredients": {"rich_text": [{"text": {"content": recipe_data['ingredients']}}]},
            "Preparation": {"rich_text": [{"text": {"content": recipe_data['preparation']}}]},
            "Video Link": {"url": recipe_data['video_url']}
        }
    )
