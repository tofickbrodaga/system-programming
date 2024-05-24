from multiprocessing import JoinableQueue, Process, Lock, synchronize, Event
import time
import random

class Client:
    def __init__(self, name: str) -> None:
        self.name = name


class Barber(Process):
    _CUTTING_TIME = 3
    def __init__(self, queue: JoinableQueue, client_came: synchronize.Event) -> None:
        super().__init__()
        self._queue = queue
        self._client_came = client_came

    def _sleep(self):
        print('Barber is sleeping')
        self._client_came.wait()
        print('barber is woken up')

    def run(self):
        while True:
            if self._queue.empty():
                self._sleep()
            client: Client = self._queue.get()
            print(f'barber is cutting hair of {client.name}')
            time.sleep(self._CUTTING_TIME)
            print(f'Barber is cutting hair of {client.name}')


class BarberShop:
    _CLIENT_INTERVAL = 1,3

    def __init__(self, clients: list[Client], queue_size: int = 3):
        self._clients = clients
        self._queue = JoinableQueue(queue_size)
        self._client_came = Event()
        self._barber = Barber(self._queue, self._client_came)
    
    def run(self) -> None:
        self._barber.start()
        for client in self._clients:
            time.sleep(random.randint(*self._CLIENT_INTERVAL))
            print(f'{client.name} comes to barbershop')
            if self._queue.full():
                print(f'{client.name} sees a full queue and LEAVES')
            elif self._queue.empty() and not self._client_came.is_set():
                print(f'{client.name} sees an empty queue a d WAKES UP the barber')
                self._client_came.set()
                self._client_came.clear()
                self._queue.put(client)
            print(f'{client.name} sits in the queue')
            self._queue.put(client)
        self._queue.join()


if __name__ == '__main__':
    clients = [Client(name) for name in ['Keanu Reeves', 'David Beckham', 'Gordon Ramsey', 'Marco Arsenovich', 'Sterlyagov S.G.']]
    time.sleep(1)
    BarberShop(clients).run()