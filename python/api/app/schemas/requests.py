from pydantic import BaseModel


class BaseRequest(BaseModel):
    # Define additional attributes or pydantic configurations here
    pass


class AssistantRequest(BaseRequest):
    question: str
