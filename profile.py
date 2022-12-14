import sys
import matplotlib.pyplot as plt
from time import time
import pickle

from single_threaded_impl import single_threaded_impl
from multi_threaded_impl_thread_pool import multi_threaded_impl

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass an input file as argument")
        sys.exit(0)

    filename = sys.argv[1]

    max_lines = 1000

    max_threads = 10
    if len(sys.argv) >= 3:
        # Ideally type check
        max_threads = int(sys.argv[2])

    try:
        with open('Storage/Expected.output', 'rb') as f:
            top_lines, top_users = pickle.load(f)
    # Support Py2
    except IOError:
        # Compute expected output if needed
        top_lines, top_users = single_threaded_impl(filename, max_lines)
        with open('Storage/Expected.output', 'wb') as f:
            pickle.dump((top_lines, top_users), f)

    # Run and time concurrent implementation
    # Threads vs processes technically an OS problem, but
    # multiple threads should be better, since we want to share memory (prices)
    samples = []
    for _ in range(5):
        start_time = time()
        top_lines_2, top_users_2 = multi_threaded_impl(filename, max_lines=1000, max_threads=max_threads)
        end_time = time()
        for line1, line2 in zip(top_lines, top_lines_2):
            assert (line1 == line2)

        for user_data, user_data_2 in zip(top_users, top_users_2):
            assert (user_data == user_data_2)

        # print("all correct")
        samples.append(end_time - start_time)

    plt.plot(samples)
    plt.show()
