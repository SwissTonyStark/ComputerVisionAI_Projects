# Receipt Interpreter Service

## Description
This service processes YouTube video URLs to extract recipe details and uploads them to a Notion database.

## Setup Instructions
1. Install dependencies:

```bash
   pip install -r requirements.txt
```

2. Configure API keys in config.yaml.
Run the server locally:
bash
Copy code
python scripts/server.py
Deployment
Deploy the project on Railway:

Push the project to a GitHub repository.
Connect the repository to Railway.
Add the following environment variables:
NOTION_API_KEY
DATABASE_ID
yaml
Copy code

---

### **Deployment on Railway**

1. Push the codebase to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
Deploy the repository on Railway:
Connect your GitHub repository.
Set the environment variables:
NOTION_API_KEY
DATABASE_ID
Railway will automatically detect server.py and start your Flask service.