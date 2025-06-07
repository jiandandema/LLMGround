import time
from vllm import LLM, AsyncLLMEngine, AsyncEngineArgs, SamplingParams

from dataModels.modelType import ModelType
from worker.BaseWorker import BaseWorker


class Worker(BaseWorker):
    def __init__(
        self,
        args,
    ):
        super().__init__(
            args.host,
            args.port,
            args.model,
            args.served_model_name,
            args.controller_url,
        )
        self._load_model(args)

    def _load_model(self, args):
        if args.task not in [ModelType.EMBED, ModelType.GENERATE]:
            raise ValueError(f"Invalid task: {args.task}")

        if args.task == ModelType.GENERATE:
            engine_args = AsyncEngineArgs(
                model=args.model,
                enforce_eager=True,
                trust_remote_code=args.trust_remote_code,
            )
            self.model = AsyncLLMEngine.from_engine_args(engine_args)
        else:
            self.model = LLM(model=args.model, trust_remote_code=args.trust_remote_code)

    async def stream(self, prompt):
        results_generator = self.model.generate(prompt, SamplingParams(), request_id=str(time.monotonic()))
        async for request_output in results_generator:
            text = request_output.outputs[0].text
            yield text

    def embed(self, prompt):
        return self.model.embed(prompt)
