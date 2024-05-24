from multiprocessing import Process, RLock, synchronize, BoundedSemaphore
import time

class SimplePhilosopher(Process):
    _DINING_TIME = 1
    _THINKING_TIME = 2
    _WAIT_TIMEOUT = 0.3

    def __init__(
            self,
            name: str,
            right_stick: synchronize.RLock,
            left_stick: synchronize.RLock,
            waiter: synchronize.BoundedSemaphore
    ) -> None:
        super().__init__()
        self.name = name
        self._right_stick = right_stick
        self._left_stick = left_stick
        self._waiter = waiter

    def print(self, text: str) -> None:
        print(f'Philosoper {self.name} {text}')

    def _think(self) -> None:
        self.print('is thinking')
        time.sleep(self._THINKING_TIME)

    def _dine(self) -> None:
        self.print('is dining')
        time.sleep(self._DINING_TIME)
    
    def _lock_and_dine(self) -> None:
        self.print('is waiting for the left stick')
        try:
            left_locked = self._left_stick.acquire(timeout=self._WAIT_TIMEOUT)
            # true - если дождались палочки, иначе false
            if left_locked:
                self.print('is waiting for the right stick')
                try:
                    right_locked = self._right_stick.acquire(timeout=self._WAIT_TIMEOUT)
                    if right_locked:
                        self._dine()
                finally:
                    if right_locked:
                        self._right_stick.release()
        finally:
            if left_locked:
                self._left_stick.release()
        self._think()

    def run(self) -> None:
        while True:
            with self._waiter:
                self._lock_and_dine()
            self._think()


if __name__ == '__main__':
    philosophers_names = (
        'Kant', 'Nieztsche', 'Diogen', 'Popper', 'Descartes',
    )
    waiter = BoundedSemaphore(len(philosophers_names)-1)
    sticks = [RLock() for _ in range(len(philosophers_names))]
    for i, name in enumerate(philosophers_names):
        SimplePhilosopher(name, sticks[i-1], sticks[i], waiter).start()
    # чтобы работало без ошибки на macOS
    time.sleep(1)
