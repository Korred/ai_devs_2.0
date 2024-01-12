import serpapi
from fastapi import APIRouter, Depends
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.services.assistant import (
    forget,
    handle_assistant_request,
    handle_search_request,
    handle_simple_assistant_request,
)
from app.core.config import settings
from app.schemas.requests import AssistantRequest
from app.schemas.responses import AssistantResponse, GenericResponse

router = APIRouter()

# Create async OpenAI client
openai_client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
)

serpapi_client = serpapi.Client(api_key=settings.SERPAPI_KEY)


# Example assistant endpoint that uses GPT-4 to answer questions
@router.post("/ask")
async def assistant(request: AssistantRequest) -> AssistantResponse:
    answer = await handle_simple_assistant_request(request, openai_client)
    return AssistantResponse(reply=answer)


@router.post("/ask-pro")
async def assistant_pro(
    request: AssistantRequest, session: AsyncSession = Depends(deps.get_session)
) -> AssistantResponse:
    answer = await handle_assistant_request(request, session, openai_client)
    return AssistantResponse(reply=answer)


@router.post("/search")
async def search(
    request: AssistantRequest, session: AsyncSession = Depends(deps.get_session)
) -> AssistantResponse:
    answer = await handle_search_request(
        request, session, openai_client, serpapi_client
    )
    return AssistantResponse(reply=answer)


@router.post("/forget")
async def forget_memories(
    session: AsyncSession = Depends(deps.get_session),
) -> GenericResponse:
    answer = await forget(session)
    return GenericResponse(message=answer)
