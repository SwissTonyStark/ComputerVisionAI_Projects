from scripts.transcriber import get_transcription

def test_transcription():
    """
    Test the transcription process with a YouTube video URL.
    """
    video_url = "https://www.youtube.com/shorts/LHcgQOw8wCU" 
    # video_url = "https://www.youtube.com/shorts/LHcgQOw8wCU" 
    try:
        print(f"Testing transcription for video: {video_url}")
        transcription = get_transcription(video_url)
        print("\nTranscription Result:")
        print(transcription)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_transcription()
