from notion_client import Client
import yaml

# Load configuration settings
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Initialize the Notion client
notion = Client(auth=config["NOTION_API_KEY"])

def send_to_notion(recipe_data):
    """
    Adds a new recipe row to an existing Notion table.
    """
    try:
        # Debug log to validate data being sent
        print(f"Sending data to Notion: {recipe_data}")

        notion.pages.create(
            parent={"database_id": config["DATABASE_ID"]},
            properties={
                "Recipe Name": {
                    "title": [
                        {"text": {"content": recipe_data["name"]}}
                    ]
                },
                "Cuisine Type": {
                    "select": {"name": recipe_data.get("cuisine", "Other")}
                },
                "Ingredients": {
                    "rich_text": [
                        {"text": {"content": recipe_data["ingredients"]}}
                    ]
                },
                "Preparation": {
                    "rich_text": [
                        {"text": {"content": recipe_data["preparation"]}}
                    ]
                },
                "Video Link": {"url": recipe_data["video_url"]},
            },
        )
        print("Data successfully sent to Notion!")
    except Exception as e:
        print(f"Error sending data to Notion: {e}")
