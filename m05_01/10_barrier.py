from random import randint
from multiprocessing import Process, Barrier, current_process
from time import sleep, ctime


def worker(barrier: Barrier):
    name = current_process().name
    print(f'Start thread {name}: {ctime()}')
    sleep(randint(1, 3))  # Имитируем какую-то работу
    barrier.wait()
    print(f'Барьер преодолен для {name}')
    print(f'End work thread {name}: {ctime()}')


if __name__ == '__main__':

    barrier = Barrier(5)

    for num in range(10):
        pr = Process(name=f'Process-{num}', target=worker, args=(barrier, ))
        pr.start()

    print('End program')
    