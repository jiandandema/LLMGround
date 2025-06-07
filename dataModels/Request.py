from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str

class EmbedRequest(BaseModel):
    prompt: str