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
    data = request.json
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({"error": "Missing video_url"}), 400

    try:
        # Process the video URL
        transcription = get_transcription(video_url)
        recipe_info = extract_recipe_info(transcription)
        send_to_notion({
            "name": "Generated Recipe",
            "ingredients": recipe_info["ingredients"],
            "preparation": recipe_info["preparation"],
            "video_url": video_url
        })

        return jsonify({"status": "success", "message": "Recipe processed successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
