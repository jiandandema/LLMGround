import argparse
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn

from dataModels.Response import Response
from dataModels.Request import EmbedRequest, GenerateRequest
from .Worker import Worker
from logger.logger import logger

# 创建 FastAPI 应用
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Worker服务已启动！"}


@app.post("/worker_generate_stream")
async def generate(request: GenerateRequest):
    generator = worker.stream(request.prompt)
    return StreamingResponse(generator)


@app.post("/worker_embed")
async def embed(request: EmbedRequest):
    res = worker.embed(request.prompt)
    response = Response(data={"embed": res})
    return JSONResponse(response.model_dump())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口号")
    parser.add_argument(
        # "--model",
        # type=str,
        # default="facebook/opt-125m",
        # help="模型名称",
        "--model",
        type=str,
        default="jinaai/jina-embeddings-v3",
        help="模型名称",
    )
    parser.add_argument(
        "--served-model-name",
        default="test",
        type=str,
        help="服务的模型名称列表",
    )
    parser.add_argument(
        "--controller-url",
        type=str,
        default="http://127.0.0.1:8001",
        help="动态负载均衡控制器地址",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="embed",
        help="任务类型",
    )
    parser.add_argument(
        "--trust_remote_code",
        type=bool,
        default=True,
        help="是否信任远程代码",
    )
    args = parser.parse_args()

    logger.info(f"启动worker服务器: {args.host}:{args.port}")
    logger.info(f"加载模型: {args.model}")
    logger.info(f"服务模型列表: {args.served_model_name}")
    logger.info(f"控制器地址: {args.controller_url}")

    worker = Worker(args)

    uvicorn.run(app, host=args.host, port=args.port)
