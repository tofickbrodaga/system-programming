import random
import time
from multiprocessing import JoinableQueue, Process, RLock, synchronize


class Instrument:
    def __init__(self, name: str, usage_time: int) -> None:
        self.name = name
        self.usage_time = usage_time
        self.lock = RLock()
    
    def use(self) -> None:
        time.sleep(self.usage_time)

class Employer(Process):
    def __init__(self, name: str, instruments: list[Instrument], queue: JoinableQueue) -> None:
        super().__init__()
        self.name = name
        self._queue = queue
        self._instruments = instruments
    
    def run(self) -> None:
        while True:
            print(f'{self.name} is waiting for a new task')
            task = self._queue.get()
            print(f'{self.name} is working on task {task}')
            for instrument in self._instruments:
                print(f"{self.name} is using {instrument.name}")
                instrument.use()


class Сhief(Process):
    _TASK_INTERVAL = 1, 2
    def __init__(self, workers_name: list[Employer], tasks: list[str]):
        self._queue = JoinableQueue
        self._init_workers()
        self._tasks = tasks
    
    def _init_workers(self, workers_name):
        instruments_data = [('hammer', .5), ('chainsaw', .7), ('laptop', 10), ('Egor Roganov', 10), ('screwed driver', 1)]
        instruments = [Instrument(name, usage_time) for name, usage_time in instruments_data]
        self._workers = [
            Employer(name, random.sample(instruments, random.randint(1, len(instruments)), self._queue))
            for name in workers_name]
        
    def run(self) -> None:
        for worker in self._workers:
            worker.start()
        
        for task in self._tasks:
            print(f'Chief has given a task {task}')
            self._queue.put(task)
        
        self._queue.join()
        print('The Bos has given a salary to his/her workers')