from vllm import LLM

from worker.BaseWorker import BaseWorker


class Worker(BaseWorker):
    def __init__(self, host, port, model, served_model_name, controller_addr):
        super().__init__(host, port, model, served_model_name, controller_addr)
        self.llm = LLM(model=model, device="cpu")
        print(self.generate(prompt="hello"))

    def generate(self, prompt):
        return self.llm.generate(prompt)
