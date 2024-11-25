from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp  # For downloading audio
import whisper

def download_audio(video_url):
    """
    Downloads audio from a YouTube video URL.
    Returns the path to the downloaded audio file.
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": "data/audio/%(id)s.%(ext)s",  # Save in audio folder
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        return f"data/audio/{info['id']}.mp3"

def get_transcription(video_url):
    """
    Retrieves transcription from a YouTube video.
    First tries subtitles; if unavailable, uses Whisper.
    """
    video_id = video_url.split("v=")[1]

    try:
        # Attempt to fetch subtitles
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es'])
        return " ".join([entry['text'] for entry in transcript])
    except:
        # If subtitles fail, use Whisper for transcription
        print("No subtitles found. Using Whisper.")
        audio_path = download_audio(video_url)
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
