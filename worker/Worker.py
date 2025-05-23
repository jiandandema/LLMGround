from vllm import LLM


class Worker(BaseWorker):
    def __init__(self, host, port, model, served_model_name):
        self.host = host
        self.port = port
        self.model = model
        self.served_model_name = served_model_name
        self.llm = LLM(model=self.model)
        # print(self.generate(prompt="你好"))
    
    def generate(self, prompt):
        return self.llm.generate(prompt)
