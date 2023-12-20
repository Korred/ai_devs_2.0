import os
from io import BytesIO

import openai
import requests
from dotenv import load_dotenv
from icecream import ic
from utils.client import AIDevsClient

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get API key from environment variables
aidevs_api_key = os.environ.get("AIDEVS_API_KEY")

# Create a client instance
client = AIDevsClient(aidevs_api_key)

# Get a task
task = client.get_task("whisper")
ic(task.data)

# Extract url from the task data 'msg' property
url_extract_msg = """
Based on the message, extract the containing URL that starts with http:// or https://.
Just return the URL, nothing else.
"""
url_completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": url_extract_msg},
        {"role": "user", "content": task.data["msg"]},
    ],
    max_tokens=60,
)

# Use the URL to download the audio file
url = url_completion.choices[0].message.content
r = requests.get(url)
audio_file = BytesIO(r.content)

# Set the name of the file to audio.mp3 so that the transcription API can recognize it
audio_file.name = "audio.mp3"

# Transcribe the audio file
tts = openai.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
)

# Get the transcription text
transcription = tts.text

# Post an answer
response = client.post_answer(task, transcription)
ic(response)
