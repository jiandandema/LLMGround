import random
import time
import threading
from typing import Dict

from fastapi import requests
from dataModels.WorkerInfo import WorkerInfo
from dataModels.WorkerHeartBeatInfo import WorkerHeartBeatInfo
from logger.logger import logger

class Controller:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.controller_addr = f"http://{self.host}:{self.port}"
        self.workers_dict: Dict[str, WorkerInfo] = {}

    def register_worker(self, info: WorkerInfo):
        if info.worker_addr in self.workers_dict:
            logger.info(f"update exist worker {info.worker_addr} register info")
        else:
            logger.info(f"register new worker {info.worker_addr} register info")
        self.workers_dict[info.worker_addr] = info
        logger.info(f"register worker {info.worker_addr} register info success")
    
    def receive_heart_beat(self, info: WorkerHeartBeatInfo):
        if info.worker_addr not in self.workers_dict:
            logger.warning(f"worker {info.worker_addr} not registered")
            return
        self.workers_dict[info.worker_addr].worker_status.queue_length = info.queue_length
        self.workers_dict[info.worker_addr].last_heart_beat_time = time.time()
        logger.info(f"receive heart beat from {info.worker_addr}")
    
    def expired_check(self):
        def del_worker_expired():
            while True:
                time.sleep(5)
                for worker_addr, worker_info in self.workers_dict.items():
                    if time.time() - worker_info.last_heart_beat_time > 20:
                        logger.warning(f"worker {worker_addr} expired")
                        del self.workers_dict[worker_addr]
        thread = threading.Thread(target=del_worker_expired, daemon=True)
        thread.start()

    def get_worer_addr(self, model_name: str):
        # 随机获取
        # TODO: 根据负载获取
        avaliable_worker = []
        for worker_addr, worker_info in self.workers_dict.items():
            if worker_info.worker_status.model_name == model_name:
                avaliable_worker.append(worker_addr)
        
        res_index = random.randint(0, len(avaliable_worker))
        return avaliable_worker[res_index]
    
    def get_stream_output(self, params):
        worker_addr = self.get_worer_addr()
        response = requests.post(
                worker_addr + "/worker_generate_stream",
                json=params,
                stream=True,
                timeout=30,
            )
        for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
            if chunk:
                yield chunk + b"\0" 
                


