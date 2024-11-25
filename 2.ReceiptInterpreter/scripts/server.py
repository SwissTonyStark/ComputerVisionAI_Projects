from flask import Flask, request, jsonify
from transcriber import get_transcription
from processor import extract_recipe_info
from notion_uploader import send_to_notion

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    """
    API endpoint for processing YouTube video URLs.
    """
    # Validate input
    data = request.get_json()
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({"error": "Missing 'video_url' in the request body"}), 400

    try:
        # Step 1: Transcribe the video
        transcription = get_transcription(video_url)
        print(f"Transcription complete: {transcription[:100]}...")  # Debugging output

        # Step 2: Extract recipe information
        recipe_info = extract_recipe_info(transcription)
        print(f"Extracted recipe info: {recipe_info}")  # Debugging output

        # Step 3: Send to Notion
        notion_data = {
            "name": recipe_info.get("name", "Generated Recipe"),  # Default name if missing
            "ingredients": recipe_info["ingredients"],
            "preparation": recipe_info["preparation"],
            "cuisine_type": recipe_info.get("cuisine", "Unknown"),
            "video_url": video_url,
            "notes": "Generated automatically from transcription"
        }
        send_to_notion(notion_data)

        return jsonify({"status": "success", "message": "Recipe processed and added to Notion!"}), 200

    except Exception as e:
        # Log and return any errors
        print(f"Error processing video: {str(e)}")  # Debugging output
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure the server is accessible from the internet
    app.run(host="0.0.0.0", port=5000)
