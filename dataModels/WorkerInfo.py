from pydantic import BaseModel

class WorkerStatus(BaseModel):
    model_name: str
    queue_length: int


class WorkerInfo(BaseModel):
    worker_addr: str
    worker_status: WorkerStatus
    last_heart_beat_time: int = -1
