import json
from openai import AsyncOpenAI
from sqlalchemy import delete, select

from app.schemas.requests import AssistantRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Memories, Messages

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
