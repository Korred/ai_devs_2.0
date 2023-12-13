import os
import openai

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
task = client.get_task("embedding")
ic(task.data)

# Define the sentence to embed
sentence = "Hawaiian pizza"

# Get the sentence embedding
# https://platform.openai.com/docs/api-reference/embeddings/create
sentence_embedding = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=sentence,
    encoding_format="float",
)
answer = sentence_embedding.data[0]["embedding"]

# Post an answer
response = client.post_answer(task, answer)
ic(response)
