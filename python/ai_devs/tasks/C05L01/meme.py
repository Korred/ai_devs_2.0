import os

import openai
from dotenv import load_dotenv
from icecream import ic
from utils.client import AIDevsClient
import httpx

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get API key from environment variables
aidevs_api_key = os.environ.get("AIDEVS_API_KEY")

# Get RenderForm API key from environment variables
renderform_api_key = os.environ.get("RENDERFORM_API_KEY")

# Create a client instance
client = AIDevsClient(aidevs_api_key)

# Get a task
task = client.get_task("meme")
ic(task.data)

# Get meme image and caption
img_url = task.data["image"]
caption = task.data["text"]


# Prior to this, we need to create a template on renderform.io and get the template id
payload = {
    "template": "meek-zombies-krump-hungrily-1970",
    "data": {
        "meme_image.src": img_url,
        "meme_caption.text": caption,
    },
}

# Create a meme using renderform.io (provide your own template id, image url and caption)
meme = httpx.post(
    "https://get.renderform.io/api/v2/render",
    json=payload,
    headers={"X-API-KEY": renderform_api_key},
)
meme_url = meme.json()["href"]
ic(meme_url)

# Post answer
response = client.post_answer(task, meme_url)
ic(response)
