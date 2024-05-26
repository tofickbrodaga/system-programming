from multiprocessing import (Barrier, Pipe, Process, Value, connection,
                             sharedctypes, synchronize)
from os import getpid


def task(
        connection: connection.Connection,
        value: int,
        operation: str,
        bound: sharedctypes.Value,
        barrier: synchronize.Barrier,
        first_to_talk: bool = True
) -> None:
    def calculate_and_send(value) -> bool:
        print(f'{pid} value before calculating: {value}')
        result = method(value, 2)
        if result > bound.value:
            return False
        print(f'{pid} value after calculating: {result}')
        connection.send(result)
        return True

    pid = getpid()
    operations = {'+': '__add__', '*': '__mul__'}
    method = getattr(int, operations[operation])

    if first_to_talk and not calculate_and_send(value):
        print(f'{pid} process deleted')
        barrier.wait()
        return
    while True:
        recv_message = connection.recv()
        if not calculate_and_send(recv_message):
            print(f'{pid} process deleted')
            barrier.wait()
            return


if __name__ == '__main__':
    value = 0
    bound = Value('i', 700)
    barrier = Barrier(2)

    conn1, conn2 = Pipe()
    Process(target=task, args=(conn1, value, '+', bound, barrier), daemon=True).start()
    Process(target=task, args=(conn2, value, '*', bound, barrier, False), daemon=True).start()
    barrier.wait()