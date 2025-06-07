import asyncio
import threading
import time
import requests

from dataModels.WorkerHeartBeatInfo import WorkerHeartBeatInfo
from dataModels.WorkerInfo import WorkerInfo, WorkerStatus
from logger.logger import logger


class BaseWorker:
    def __init__(
        self,
        host,
        port,
        model_path,
        served_model_name,
        controller_addr,
        limit_worker_concurrency=1024,
    ):
        self.host = host
        self.port = port
        self.model_path = model_path
        self.served_model_name = served_model_name
        self.limit_worker_concurrency = limit_worker_concurrency
        self.semaphore = asyncio.Semaphore(self.limit_worker_concurrency)
        self.heart_beat_thread = None
        self.worker_addr = f"http://{self.host}:{self.port}"
        self.controller_addr = controller_addr
        self.init_heart_beat()

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
                time.sleep(10)
                obj.send_heart_beat()

        self.register_to_contoller()
        self.heart_beat_thread = threading.Thread(
            target=heart_beat_worker, args=(self,), daemon=True
        )
        self.heart_beat_thread.start()

    def register_to_contoller(self):
        url = self.controller_addr + "/register_worker"
        register_worker_info = WorkerInfo(
            worker_addr=self.worker_addr,
            worker_status=self.get_status(),
            last_heart_beat_time=time.time(),
        )
        r = requests.post(url, json=register_worker_info.model_dump())
        assert r.status_code == 200

    def send_heart_beat(self):
        url = self.controller_addr + "/receive_heart_beat"

        while True:
            try:
                heart_beat_info = WorkerHeartBeatInfo(
                    worker_addr=self.worker_addr, queue_length=self.get_queue_length()
                )
                ret = requests.post(
                    url,
                    json=heart_beat_info.model_dump(),
                    timeout=5,
                )
                break
            except (requests.exceptions.RequestException, KeyError) as e:
                # logger.error(f"heart beat error: {e}")
                pass
            time.sleep(10)

    def get_queue_length(self):
        if self.semaphore is None:
            return 0
        else:
            sempahore_value = (
                self.semaphore._value
                if self.semaphore._value is not None
                else self.limit_worker_concurrency
            )
            waiter_count = (
                0 if self.semaphore._waiters is None else len(self.semaphore._waiters)
            )
            return self.limit_worker_concurrency - sempahore_value + waiter_count

    def get_status(self):
        return WorkerStatus(
            model_name=self.served_model_name, queue_length=self.get_queue_length()
        )
