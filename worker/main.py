import argparse
import logging
import sys
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from Worker import Worker

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI()


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/")
async def root():
    return {"message": "模型服务已启动"}


@app.post("/generate")
async def generate(request: GenerateRequest):
    return worker.generate(request.prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口号")
    parser.add_argument(
        "--model", type=str, default="facebook/opt-125m", help="模型名称"
    )
    parser.add_argument(
        "--served-model-name",
        nargs="+",
        default=["test"],
        type=str,
        help="服务的模型名称列表",
    )
    parser.add_argument(
        "--controller-url",
        nargs="+",
        type=str,
        default=["http://127.0.0.1:8000"],
        help="动态负载均衡控制器地址",
    )
    args = parser.parse_args()

    logger.info(f"启动服务器: {args.host}:{args.port}")
    logger.info(f"加载模型: {args.model}")
    logger.info(f"服务模型列表: {args.served_model_name}")
    logger.info(f"控制器地址: {args.controller_url}")

    worker = Worker(args.host, args.port, args.model, args.served_model_name)

    uvicorn.run(app, host=args.host, port=args.port)
