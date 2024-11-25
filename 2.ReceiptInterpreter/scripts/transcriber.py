from transformers import pipeline
import yt_dlp
import os
from pydub import AudioSegment

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

def split_audio(audio_path, segment_length_ms=30000):
    """
    Splits audio into smaller segments to avoid processing limits.
    """
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)

    segments = []
    for start in range(0, duration_ms, segment_length_ms):
        end = min(start + segment_length_ms, duration_ms)
        segment = audio[start:end]
        segment_path = f"{audio_path}_segment_{start // 1000}-{end // 1000}.mp3"
        segment.export(segment_path, format="mp3")
        segments.append(segment_path)
    return segments

def transcribe_audio_segments(audio_segments):
    """
    Transcribes a list of audio segments using a Hugging Face model.
    Returns the concatenated transcription.
    """
    try:
        asr_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base")
        transcriptions = []

        for segment in audio_segments:
            result = asr_pipeline(segment)
            transcriptions.append(result["text"])

            # Clean up the segment file after processing
            if os.path.exists(segment):
                os.remove(segment)

        return " ".join(transcriptions)
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe audio: {str(e)}")

def get_transcription(video_url):
    """
    Full pipeline: downloads the audio, splits it into segments, and transcribes.
    """
    try:
        # Step 1: Download audio
        audio_path = download_audio(video_url)
        # Step 2: Split audio into smaller segments
        audio_segments = split_audio(audio_path)
        # Step 3: Transcribe each segment and concatenate results
        transcription = transcribe_audio_segments(audio_segments)
        # Step 4: Clean up original audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return transcription
    except Exception as e:
        raise RuntimeError(f"Transcription pipeline failed: {str(e)}")
