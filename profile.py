import sys
import matplotlib.pyplot as plt
from time import time

from single_threaded_impl import single_threaded_impl
from multi_threaded_impl import multi_threaded_impl

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass an input file as argument")
        sys.exit(0)

    filename = sys.argv[1]

    max_lines = None
    if len(sys.argv) >= 3:
        # Ideally type check
        max_lines = int(sys.argv[2])

    # single threaded is roughly 2s per network call

    # Run and time concurrent implementation
    # Threads vs processes technically an OS problem, but
    # multiple threads should be better, since we want to share memory (prices)
    samples = []
    for power in range(max_lines):
        start_time = time()
        top_lines, top_users = multi_threaded_impl(filename, 10 ** power)
        end_time = time()
        samples.append(end_time - start_time)

    plt.plot(samples)
    plt.show()
