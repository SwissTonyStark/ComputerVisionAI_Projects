from flask import Flask, request, jsonify
from transcriber import get_transcription
from processor import extract_recipe_info
from notion_uploader import send_to_notion
import logging

app = Flask(__name__)

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route('/process', methods=['POST'])
def process_video():
    """
    API endpoint to process YouTube Shorts video URLs.
    Receives a video URL, extracts transcription, processes the recipe, and uploads to Notion.
    """
    try:
        # Log incoming request
        logging.info("Received request: %s", request.json)

        # Get video URL from the request
        data = request.json
        video_url = data.get('video_url')
        if not video_url:
            return jsonify({"error": "Missing video_url in request"}), 400

        # Validate the URL format
        if 'youtube.com/shorts/' not in video_url:
            return jsonify({"error": "Invalid YouTube Shorts URL"}), 400

        # Log start of transcription
        logging.info("Starting transcription for URL: %s", video_url)
        transcription = get_transcription(video_url)
        logging.info("Transcription completed successfully.")

        # Process the transcription to extract recipe details
        logging.info("Processing transcription to extract recipe details...")
        recipe_data = extract_recipe_info(transcription)
        logging.info("Recipe details extracted: %s", recipe_data)

        # Add metadata to recipe data
        recipe_data["name"] = "Generated Recipe"  # Placeholder for now
        recipe_data["video_url"] = video_url

        # Upload recipe to Notion
        logging.info("Uploading recipe to Notion...")
        send_to_notion(recipe_data)
        logging.info("Recipe successfully uploaded to Notion.")

        return jsonify({"status": "success", "message": "Recipe processed successfully!"}), 200

    except Exception as e:
        # Log the error and return a failure response
        logging.error("An error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use this for local development
    app.run(host="0.0.0.0", port=5000, debug=True)

    # Comment this line when running locally, and uncomment for Railway.app
    # app.run()