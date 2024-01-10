import json
import os

import openai
from dotenv import load_dotenv
from icecream import ic
from utils.client import AIDevsClient
import httpx

from itertools import islice


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get API key from environment variables
aidevs_api_key = os.environ.get("AIDEVS_API_KEY")

# Create a client instance
client = AIDevsClient(aidevs_api_key)

# Get a task
task = client.get_task("optimaldb")
ic(task.data)

big_json = httpx.get(task.data["database"]).json()
ic(big_json)

summary_msg = """
Given a list of sentences, summarize/condense it to be as short as possible while retaining the original meaning.
Consider the following methods:
1. Translate the sentences to English
2. Remove all unnecessary words, e.g. "a", "the", "at", "as", "be" etc.
3. Remove all unnecessary information, e.g. "I think that", "I believe that" etc.
4. The summary should be as short as possible, it does not have to be a full sentence (e.g. it can be a noun phrase).
5. Remove all quotation marks, apostrophes, dots
6. IMPORTANT: ONE SENTENCE PER LINE (separated by a newline character)

Example: 
Sentence: Podczas ostatniej konferencji technologicznej, program który stworzył Zygfryd wygrał nagrodę za innowacyjność w użyciu JavaScript.
Summary: last tech conference, crated program won javascript innovation award

Sentence: Jeden z ulubionych filmów Zygfryda to 'Matrix', który ogląda co najmniej dwa razy do roku.
Summary: favorite movie matrix, watch at least twice a year

Sentence: Zygfryd jest bardzo dobrym programistą, który zawsze stara się pomóc innym.
Summary: good programmer, always tries to help others

Sentence: Na swój weselny taniec, Zygfryd wybrał klasycznego tanga
Summary: wedding dance, chose classic tango

Only return the summary, do not return the original sentence and do not provide any additional information / thoughts.
One sentence per line (separated by a newline character).
"""


intial_summaries = []
for person, sentences in big_json.items():
    summaries = []

    for data in chunk(sentences, 10):
        joined = " ".join(data)
        sentence_summary = (
            openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": summary_msg},
                    {"role": "user", "content": joined},
                ],
                max_tokens=1000,
            )
            .choices[0]
            .message.content
        )

        summaries.append(sentence_summary)

    intial_summaries.append(
        f"Information for {person}:\n####\n" + "\n".join(summaries) + "\n####"
    )


initial_summary = "\n\n".join(intial_summaries)


system_msg = """
Given a list of facts about a person, summarize it to be as short as possible while retaining the original meaning.
Do not drop important facts like favourite movies, games, books etc. Instead, remove stop words like (as, for, in, the, a, an)
and unnecessary information like "I think that", "I believe that" etc.
If possible, create a list of facts instead of a paragraph e.g. likes, dislikes, hobbies, favourite movies, favourite books etc.
The goal is to create a summary that is as short as possible (shorter than the original text) while retaining the original meaning.
Return in the same format as the input but with the summary instead of the original sentences/facts.
"""


summarize_total = (
    openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": initial_summary},
        ],
        max_tokens=4000,
    )
    .choices[0]
    .message.content
)

ic(summarize_total)

# Post answer
response = client.post_answer(task, summarize_total)
ic(response)
