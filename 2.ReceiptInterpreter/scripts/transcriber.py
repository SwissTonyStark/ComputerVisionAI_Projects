from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp  # For downloading audio
import whisper
import os

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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return f"data/audio/{info['id']}.mp3"
    except Exception as e:
        raise RuntimeError(f"Failed to download audio: {str(e)}")

def get_transcription(video_url, whisper_model="base"):
    """
    Retrieves transcription from a YouTube video.
    First tries subtitles; if unavailable, uses Whisper.
    """
    video_id = video_url.split("v=")[1]

    try:
        # Attempt to fetch subtitles
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es'])
        return " ".join([entry['text'] for entry in transcript])
    except Exception:
        print("No subtitles found. Using Whisper for transcription.")
        try:
            audio_path = download_audio(video_url)
            model = whisper.load_model(whisper_model)
            result = model.transcribe(audio_path)

            # Clean up the audio file after transcription
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return result["text"]
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
