import json
import os

import openai
from dotenv import load_dotenv
from icecream import ic
from utils.client import AIDevsClient
from datetime import datetime, timedelta
from typing import Union


def next_weekday(
    d: datetime, weekday: int, as_string: bool = False
) -> Union[datetime, str]:
    days = (weekday - d.weekday() + 7) % 7
    date = d + timedelta(days=days)

    if as_string:
        return date.strftime("%Y-%m-%d")
    return date


# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get API key from environment variables
aidevs_api_key = os.environ.get("AIDEVS_API_KEY")

# Create a client instance
client = AIDevsClient(aidevs_api_key)

# Get a task
task = client.get_task("tools")
ic(task.data)

# Define some additional context for the system which might be hard to calculate
system_msg = f"""
Additional context:
- Today is {datetime.today().strftime('%Y-%m-%d')}
- The next weekday dates are:
    - Monday: {next_weekday(datetime.today(), 0, True)}
    - Tuesday: {next_weekday(datetime.today(), 1, True)}
    - Wednesday: {next_weekday(datetime.today(), 2, True)}
    - Thursday: {next_weekday(datetime.today(), 3, True)}
    - Friday: {next_weekday(datetime.today(), 4, True)}
    - Saturday: {next_weekday(datetime.today(), 5, True)}
    - Sunday: {next_weekday(datetime.today(), 6, True)}
"""

# Define function specifications
functions = [
    {
        "type": "function",
        "function": {
            "name": "intentToolRecognition",
            "description": "Returns the intent of a given text and which tool to use e.g. create a ToDo item or create a calendar event",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "enum": ["ToDo", "Calendar"],
                        "description": "Name of the tool to use e.g. if the text includes a date/time information use 'Calendar' otherwise use 'ToDo'. Tool is mandatory!",
                    },
                    "desc": {
                        "type": "string",
                        "description": "Normalized description of the ToDo item or Calendar event e.g. 'Kupic mleko' -> 'Kup mleko' or 'Umow wizite u lekarza na 10:00' -> 'Wizyta u lekarza'",
                    },
                    "date": {
                        "type": "string",
                        "description": "Should be a date in ISO 8601 format (e.g. 2021-09-30) and only if the Calendar tool should be used, otherwise skip this property",
                    },
                },
            },
            "required": ["tool", "desc"],
        },
    }
]

# Figure out which tool to use
intent = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": task.data["question"]},
    ],
    tools=functions,
    max_tokens=200,
)

# Extract arguments for the function
answer = intent.choices[0].message.tool_calls[0].function.arguments
answer = json.loads(answer)
ic(answer)

# Post the answer
response = client.post_answer(task, answer)
ic(response)
