# LLMGround

LLMGround 是一个基于 vLLM 的分布式大语言模型服务框架，支持模型推理和嵌入任务。

## 功能特点

- 支持多种模型任务类型（生成、嵌入）
- 基于 FastAPI 的异步 Web 服务
- 分布式部署支持
- 动态负载均衡
- 流式输出支持

## 系统要求

- Python 3.10+
- CUDA 支持的 GPU
- 足够的 GPU 显存（取决于模型大小）

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/LLMGround.git
cd LLMGround
```

2. 创建并激活虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 启动 Worker 服务

```bash
python -m worker.main \
    --host 127.0.0.1 \
    --port 8000 \
    --model facebook/opt-125m \
    --served-model-name test \
    --controller-url http://127.0.0.1:8001 \
    --task generate \
    --trust_remote_code True
```

参数说明：
- `--host`: 服务器主机地址
- `--port`: 服务器端口号
- `--model`: 模型名称
- `--served-model-name`: 服务的模型名称
- `--controller-url`: 动态负载均衡控制器地址
- `--task`: 任务类型（generate/embed）
- `--trust_remote_code`: 是否信任远程代码

### API 接口

#### 流式生成接口

```bash
POST /worker_generate_stream
Content-Type: application/json

{
    "prompt": "你的提示词"
}
```

## 项目结构

```
LLMGround/
├── controller/     # 负载均衡控制器
├── dataModels/     # 数据模型定义
├── logger/         # 日志模块
├── models/         # 模型相关代码
├── worker/         # Worker 服务实现
├── main.py         # 主程序入口
└── pyproject.toml  # 项目配置文件
```

## 开发

### 代码风格

项目使用 Ruff 进行代码格式化和检查。在提交代码前，请运行：

```bash
ruff check .
ruff format .
```

## 许可证

[待定]

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

[待定]
