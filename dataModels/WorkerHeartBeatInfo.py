from pydantic import BaseModel

class WorkerHeartBeatInfo(BaseModel):
    worker_addr: str
    queue_length: int