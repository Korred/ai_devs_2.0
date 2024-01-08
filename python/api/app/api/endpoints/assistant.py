from openai import AsyncOpenAI
from fastapi import APIRouter, Depends
from app.schemas.responses import AssistantResponse, GenericResponse
from app.schemas.requests import AssistantRequest
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.services.assistant import (
    handle_assistant_request,
    forget,
    handle_simple_assistant_request,
)

router = APIRouter()

# Create async OpenAI client
openai_client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
)


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


@router.post("/forget")
async def forget_memories(
    session: AsyncSession = Depends(deps.get_session),
) -> GenericResponse:
    answer = await forget(session)
    return GenericResponse(message=answer)
