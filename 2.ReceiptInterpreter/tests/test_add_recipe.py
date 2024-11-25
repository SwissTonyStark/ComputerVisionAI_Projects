from notion_client import Client
import yaml

# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Initialize Notion client
notion = Client(auth=config["NOTION_API_KEY"])

# Function to add a new recipe
def add_recipe_to_notion(recipe_data):
    try:
        response = notion.pages.create(
            parent={"database_id": config["DATABASE_ID"]},
            properties={
                "Recipe Name": {
                    "title": [
                        {"text": {"content": recipe_data["name"]}}
                    ]
                },
                "Cuisine Type": {
                    "select": {"name": recipe_data.get("cuisine_type", "Other")}
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
                "Notes": {
                    "rich_text": [
                        {"text": {"content": recipe_data.get("notes", "")}}
                    ]
                },
            },
        )
        print("Recipe added successfully!")
        print(response)
    except Exception as e:
        print(f"Error adding recipe: {e}")

# Example recipe data
recipe_data = {
    "name": "Spaghetti Carbonara",
    "cuisine_type": "Italian",
    "ingredients": "Spaghetti, Eggs, Parmesan Cheese, Bacon, Black Pepper",
    "preparation": "Boil spaghetti. Mix eggs and cheese. Fry bacon. Combine everything.",
    "video_url": "https://www.youtube.com/watch?v=example",
    "notes": "Quick and delicious!",
}

# Add the recipe
add_recipe_to_notion(recipe_data)
