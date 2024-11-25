from notion_client import Client
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Inicializar cliente de Notion
notion = Client(auth=config["NOTION_API_KEY"])

# Probar conexión con la base de datos
database_id = config["DATABASE_ID"]

try:
    response = notion.databases.retrieve(database_id=database_id)
    print("Connection successful!")
    print(response)  # Muestra la estructura de la base de datos
except Exception as e:
    print(f"Error connecting to Notion: {e}")
