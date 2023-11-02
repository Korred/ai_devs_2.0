import os

from dotenv import load_dotenv
from icecream import ic
from utils.client import AIDevsClient

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
aidevs_api_key = os.environ.get("AIDEVS_API_KEY")

# Create a client instance
client = AIDevsClient(aidevs_api_key)

# Get a task
task = client.get_task("helloapi")
ic(task.data)

# Post an answer
response = client.post_answer(task, task.data["cookie"])
ic(response)
