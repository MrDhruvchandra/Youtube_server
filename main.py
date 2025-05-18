from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable, NoTranscriptFound

app = FastAPI()

def fetch_transcript(video_id: str) -> str:
    """
    Fetches the transcript of a YouTube video by its video ID.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        str: A single string containing the full transcript text.
    """
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
        
        # Join all transcript text into a single string
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return full_transcript
    except TranscriptsDisabled:
        raise HTTPException(status_code=400, detail="Transcripts are disabled for this video.")
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="The video is unavailable.")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No transcript found for this video.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    """
    API endpoint to fetch the transcript of a YouTube video.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        dict: A dictionary containing the transcript text.
    """
    transcript = fetch_transcript(video_id)
    return {"video_id": video_id, "transcript": transcript}