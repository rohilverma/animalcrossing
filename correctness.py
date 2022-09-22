import sys
import os
import pickle

from single_threaded_impl import single_threaded_impl
from multi_threaded_impl import multi_threaded_impl


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass an input file as argument")
        sys.exit(0)

    filename = sys.argv[1]

    max_lines = 1000

    max_iterations = None
    if len(sys.argv) >= 3:
        # Ideally type check
        max_iterations = int(sys.argv[2])

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
    for n in range(max_iterations):
        top_lines_2, top_users_2 = multi_threaded_impl(filename, max_lines)

        for line1, line2 in zip(top_lines, top_lines_2):
            assert(line1 == line2)

        for user_data, user_data_2 in zip(top_users, top_users_2):
            assert(user_data == user_data_2)

    print("all asserts passed for "+str(n+1)+" iterations!")
