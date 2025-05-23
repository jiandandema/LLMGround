import asyncio
import threading
import time

from fastapi import requests

class BaseWorker:
    def __init__(self, host, port, model, served_model_name, limit_worker_concurrency=1024):
        self.host = host
        self.port = port
        self.model = model
        self.served_model_name = served_model_name
        self.semaphore = asyncio.Semaphore(self.limit_worker_concurrency)
        self.limit_worker_concurrency = limit_worker_concurrency
        self.heart_beat_thread = None

    
    def invoke(self, prompt):
        raise NotImplementedError

    def stream(self, prompt):
        raise NotImplementedError
    
    def embed(self, str):
        raise NotImplementedError
    
    def release_worker_semaphore(self):
        self.semaphore.release()

    def acquire_worker_semaphore(self):
        return self.semaphore.acquire()

    def init_heart_beat(self):
        def heart_beat_worker(obj):
            while True:
                time.sleep(5)
                obj.send_heart_beat()
        self.register_to_contoller()
        self.heart_beat_thread = threading.Thread(target=heart_beat_worker, args=(self,), daemon=True)
        self.heart_beat_thread.start()
    
    def register_to_contoller(self):
        url = self.controller_addr + "/register_worker"
        # data = {
        #     "worker_name": self.worker_addr,
        #     "check_heart_beat": True,
        #     "worker_status": self.get_status(),
        #     "multimodal": self.multimodal,
        # }
        # 这里需要根据我制定的协议来发送数据
        data = {}
        r = requests.post(url, json=data)
        assert r.status_code == 200
    
    def send_heart_beat(self):
        url = self.controller_addr + "/receive_heart_beat"
        
        while True:
            try:
                ret = requests.post(
                    url,
                    json={
                        "worker_name": self.worker_addr,
                        "queue_length": self.get_queue_length(),
                    },
                    timeout=5,
                )
                exist = ret.json()["exist"]
                break
            except (requests.exceptions.RequestException, KeyError) as e:
                # logger.error(f"heart beat error: {e}")
                pass
            time.sleep(5)
