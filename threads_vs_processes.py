import requests
import time
from threading import Thread

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


def task():
    requests.get("http://www.acnhapi.com/v1/fish/10")


def variant1(n_tasks=1000):
    s = time.time()
    threads = []
    for _ in range(n_tasks):
        thread = Thread(target=task)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    e = time.time()
    return e - s


def variant2(n_tasks=1000, n_workers=1000):
    s = time.time()
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        for _ in range(n_tasks):
            executor.submit(task)
    e = time.time()
    return e - s


def variant3(n_tasks=1000, n_processes=1000):
    s = time.time()
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        for _ in range(n_tasks):
            executor.submit(task)
    e = time.time()
    return e - s


def shard(tasks_per_shard: int):
    with ThreadPoolExecutor(max_workers=tasks_per_shard) as executor:
        for _ in range(tasks_per_shard):
            executor.submit(task)


def variant4(n_tasks=1000, n_processes=10):
    s = time.time()
    tasks_per_shard = n_tasks // n_processes
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        for _ in range(n_processes):
            executor.submit(shard, tasks_per_shard)
    e = time.time()
    return e - s


if __name__ == "__main__":
    for ExecClass in [ThreadPoolExecutor, ProcessPoolExecutor]:
        samples = []
        for _ in range(5):
            s = time.time()
            futures = []
            with ExecClass(max_workers=3) as executor:
                futures.append(executor.submit(variant1))
                futures.append(executor.submit(variant2))
                futures.append(executor.submit(variant4, 1000, 10))

            for future in futures:
                print(future.result())
            e = time.time()
            samples.append(e - s)
        print("Final times: ", samples, ExecClass)
    # Many different errors, ex: Queue.Full, MemoryError, Paging file full
    # print(variant3(n_processes=50))

    # Individual times in serial were 2s, 2s, 4s:  Total: 8s
    # With concurrent processes were 6s, 6s, 6s; total: 6.5s
    # Final times:  [6.735992908477783, 6.953444719314575, 6.653178691864014,
    # 7.547821760177612, 6.40388035774231] <class 'concurrent.futures.process.ProcessPoolExecutor'>
    # With concurrent threads were 9s, 9s, 3s; total 9.2s
    # Final times:  [18.336066246032715, 13.265495777130127, 11.788486003875732,
    # 11.461360692977905, 14.65581750869751] <class 'concurrent.futures.thread.ThreadPoolExecutor'>

    # Why spinning up processes faster? Shouldn't really be any difference since tasks are the same
    # (Run a bunch of threads, and run some processes with threads).
