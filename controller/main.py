import argparse
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from .Controller import Controller
from dataModels.WorkerHeartBeatInfo import WorkerHeartBeatInfo
from dataModels.WorkerInfo import WorkerInfo
from logger.logger import logger
# 创建 FastAPI 应用
app = FastAPI()


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/")
async def root():
    return {"message": "Controller服务已启动！"}

@app.post("/register_worker")
async def register_worker(request: Request, worker_info: WorkerInfo):
    return await controller.register_worker(info=worker_info)

@app.post("/receive_heart_beat")
async def recv_heart_beat(request: Request, worker_heart_beat_info: WorkerHeartBeatInfo):
    return await controller.receive_heart_beat(info=worker_heart_beat_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8001, help="服务器端口号")
    args = parser.parse_args()

    logger.info(f"启动controller服务器: {args.host}:{args.port}")

    controller = Controller(args.host, args.port)

    uvicorn.run(app, host=args.host, port=args.port)
