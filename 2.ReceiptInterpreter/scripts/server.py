from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/process', methods=['POST'])
def process_video():
    try:
        # Log incoming request
        logging.info("Received request: %s", request.json)

        # Get the JSON payload from the request
        data = request.json
        if not data or 'video_url' not in data:
            return jsonify({"error": "Missing video_url in request"}), 400

        video_url = data['video_url']

        # Check if the URL is a valid YouTube Shorts link
        if 'youtube.com/shorts/' not in video_url:
            return jsonify({"error": "Invalid YouTube Shorts URL"}), 400

        # Extract the video ID
        video_id = extract_shorts_id(video_url)
        if not video_id:
            return jsonify({"error": "Failed to extract video ID"}), 400

        # Simulate video analysis or processing
        result = analyze_shorts_video(video_id)

        return jsonify({
            "message": "Video processed successfully",
            "video_id": video_id,
            "result": result
        }), 200

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500


def extract_shorts_id(url):
    """
    Extract the video ID from a YouTube Shorts URL.
    """
    try:
        # Assume Shorts URLs are always in the format: youtube.com/shorts/<id>
        return url.split('shorts/')[1].split('?')[0]
    except IndexError:
        return None


def analyze_shorts_video(video_id):
    """
    Simulate the analysis or processing of a Shorts video.
    """
    # Placeholder for real logic; return dummy data for now.
    return {"video_id": video_id, "status": "analyzed"}


if __name__ == '__main__':
    # Use this for local development
    app.run(host="0.0.0.0", port=5000, debug=True)

    # Comment this line when running locally, and uncomment for Railway.app
    # app.run()