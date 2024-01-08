from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    # https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)


class GenericResponse(BaseResponse):
    message: str


class AssistantResponse(BaseResponse):
    reply: str
