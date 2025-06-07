from pydantic import BaseModel


class Response(BaseModel):
    code: int = 1
    data: dict = {}
    msg: str = ""
