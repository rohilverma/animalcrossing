import requests
import time
from threading import Thread

from urllib3 import PoolManager, HTTPConnectionPool


def task():
    requests.get("http://www.acnhapi.com/v1/fish/10")


def task2(pool_manager: PoolManager):
    pool_manager.request("GET", "http://www.acnhapi.com/v1/fish/10")


def task3(pool: HTTPConnectionPool):
    pool.request("GET", "http://www.acnhapi.com/v1/fish/10")


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


def variant2(n_tasks=1000):
    s = time.time()
    threads = []
    with PoolManager() as pool_manager:
        for _ in range(n_tasks):
            thread = Thread(target=task2, args=(pool_manager,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    e = time.time()
    return e - s


def variant3(n_tasks=1000, n_pool_size=1):
    s = time.time()
    threads = []
    with HTTPConnectionPool("www.acnhapi.com", maxsize=n_pool_size) as pool:
        for _ in range(n_tasks):
            thread = Thread(target=task3, args=(pool,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    e = time.time()
    return e - s


if __name__ == "__main__":
    n_tasks = 4000
    print("Threading", variant1(n_tasks=n_tasks))
    print("PoolManager + ConnectionPool (1)", variant2(n_tasks=n_tasks))
    print("ConnectionPool (1)", variant3(n_tasks=n_tasks))
    print("ConnectionPool (5)", variant3(n_tasks=n_tasks, n_pool_size=5))
    print("ConnectionPool (10)", variant3(n_tasks=n_tasks, n_pool_size=10))
    print("ConnectionPool (15)", variant3(n_tasks=n_tasks, n_pool_size=15))
    print("ConnectionPool (20)", variant3(n_tasks=n_tasks, n_pool_size=20))
    print("ConnectionPool (25)", variant3(n_tasks=n_tasks, n_pool_size=25))
    print("ConnectionPool (30)", variant3(n_tasks=n_tasks, n_pool_size=30))
    print("ConnectionPool (35)", variant3(n_tasks=n_tasks, n_pool_size=35))
    print("ConnectionPool (40)", variant3(n_tasks=n_tasks, n_pool_size=40))
