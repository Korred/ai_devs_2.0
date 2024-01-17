import json

import serpapi
from openai import AsyncOpenAI
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Memories, Messages
from app.schemas.requests import AssistantRequest

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "intentRecognition",
            "description": "Returns the intent of a given text and which tool to use e.g. answer a generic (non-user specific), answer a user specific question or store a fact about the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "enum": ["GenericQuestion", "UserQuestion", "UserFact"],
                        "description": "Required - Name of the tool to use e.g. 'GenericQuestion' for non-user specific questions, 'UserQuestion' for user specific questions and 'UserFact' for facts about the user.",
                    },
                    "message": {
                        "type": "string",
                        "description": "Required - The user message to process e.g. 'What is the weather in Warsaw?' or 'What is my name?' or 'My name is John'",
                    },
                },
            },
            "required": ["tool", "message"],
        },
    }
]


async def intent_recognition(message: str, openai_client: AsyncOpenAI) -> dict:
    system_msg = "Use the defined tools to handle the user message. Please remember, the 'tool' and 'message' properties are mandatory and must be provided!"

    intent_check = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": system_msg,
            },
            {"role": "user", "content": message},
        ],
        tools=TOOLS,
        max_tokens=200,
    )
    intent = intent_check.choices[0].message.tool_calls[0].function.arguments
    intent = json.loads(intent)

    return intent


async def handle_generic_message(message: str, openai_client: AsyncOpenAI) -> str:
    completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": message},
        ],
        max_tokens=200,
    )

    answer = completion.choices[0].message.content
    return answer


async def handle_user_question(
    message: str, session: AsyncSession, openai_client: AsyncOpenAI
) -> str:
    # Fetch the latest 15 user facts from the database
    memories = await session.execute(select(Memories).limit(15))

    context = "\n".join([f"- '{m.content}'" for m in memories.scalars().all()])
    system_msg = f"Answer the provided question about the user, based on the provided context: {context} \n If you don't know the answer, just say 'I don't know' and nothing else!"

    completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": message},
        ],
        max_tokens=200,
    )

    answer = completion.choices[0].message.content
    return answer


async def store_user_fact(message: str, session: AsyncSession) -> str:
    fact = Memories(content=message)
    session.add(fact)
    await session.commit()

    return "Thanks, I will remember that!"


async def handle_simple_assistant_request(
    request: AssistantRequest, openai_client: AsyncOpenAI
) -> str:
    completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": request.question},
        ],
        max_tokens=200,
    )

    answer = completion.choices[0].message.content
    return answer


async def handle_assistant_request(
    request: AssistantRequest, session: AsyncSession, openai_client: AsyncOpenAI
) -> str:
    intent = await intent_recognition(request.question, openai_client)

    if intent["tool"] == "GenericQuestion":
        answer = await handle_generic_message(request.question, openai_client)

    elif intent["tool"] == "UserQuestion":
        answer = await handle_user_question(request.question, session, openai_client)

    elif intent["tool"] == "UserFact":
        answer = await store_user_fact(request.question, session)

    await store_conversation(request.question, answer, session)

    return answer


async def forget(session: AsyncSession) -> str:
    await session.execute(delete(Memories))
    await session.commit()

    return "All memories have been forgotten!"


async def store_conversation(question: str, answer: str, session: AsyncSession):
    fact = Messages(question=question, answer=answer)
    session.add(fact)
    await session.commit()


async def handle_md2html_request(
    request: AssistantRequest,
    session: AsyncSession,
    openai_client: AsyncOpenAI,
) -> str:
    system_msg = """
    Translate the provided markdown into html.
    Return only the html content, nothing else.
    Ensure that the href tag is using the double quotation mark instead of a single one.
    """

    completion = await openai_client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8hkZbTOZ",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": request.question},
        ],
        max_tokens=400,
    )

    answer = completion.choices[0].message.content

    await store_conversation(request.question, answer, session)

    return answer


async def handle_search_request(
    request: AssistantRequest,
    session: AsyncSession,
    openai_client: AsyncOpenAI,
    serpapi_client: serpapi.Client,
) -> str:
    system_msg = """
    You will be provided with a question about a website url the user is interested in.
    Translate the question into a google search query that will return the most relevant result.
    
    IMPORTANT: The question might be in a different language than English.
    Ensure that the google search query is in the same language as the question.
    
    Reply in the following format:
    {
        "query": "google search query",
        "location": "search origin country",
        "gl": "google search two letter country code",
        "hl": "google search two letter language code"
    }
    
    Example:    
    Q: Potrzebuje adres do strony na wikipedii o H.P. Lovecraft
    A: {
        "query": "H.P. Lovecraft wikipedia",
        "location": "Poland",
        "gl": "pl",
        "hl": "pl"
    }
    
    Q: I need the subreddit for the game Cyberpunk 2077
    A: {
        "query": "Cyberpunk 2077 subreddit",
        "location": "United States",
        "gl": "us",
        "hl": "en"
    }
    
    Q: Wo finde ich Informationen über den neusten Chaos Computer Club Congress?
    A: {
        "query": "Chaos Computer Club Congress 2023",
        "location": "Germany",
        "gl": "de",
        "hl": "de"
    }
    """

    completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": request.question},
        ],
        max_tokens=400,
    )

    response = completion.choices[0].message.content

    await store_conversation(request.question, response, session)

    data = json.loads(response)
    results = serpapi_client.search(
        q=data["query"],
        location=data["location"],
        gl=data["gl"],
        hl=data["hl"],
    )

    top_5_urls = [result["link"] for result in results["organic_results"][:5]]

    url_chooser_msg = f"""
    Question: {request.question}
    Google Search Query: {data["query"]}
    
    Given the question and the google search query, choose the most relevant url from the top 5 results:
    {top_5_urls}
    
    Just reply with the url you think is the most relevant.
    """

    print(top_5_urls)

    url_completion = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": url_chooser_msg},
        ],
        max_tokens=300,
    )

    answer = url_completion.choices[0].message.content

    await store_conversation(url_chooser_msg, answer, session)

    return answer
