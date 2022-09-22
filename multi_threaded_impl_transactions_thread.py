import json
from typing import List, Any, Dict, Union, Tuple
import requests
from time import time
import threading

cost_dict: Dict[str, int] = {}

line_lock = threading.Lock()
# this could be made more fine-grained on a user-id level
user_lock = threading.Lock()


def process_transaction(key_prefix: str, item_id: int, index: int, qty: int, outputs: List[int]):
    key = key_prefix + str(item_id)
    r = requests.get("http://www.acnhapi.com/v1/" + key_prefix + "/" + str(item_id))
    price = r.json()['price']
    cost_dict[key] = price
    outputs[index] = price * qty


def cost_of_transactions(transactions: List[Union[str, List[Union[str, int]]]]) -> int:
    outputs = [0 for _ in range(len(transactions))]
    threads = []
    for index, transaction in enumerate(transactions):
        if type(transaction) is list:
            item_type, item_id, qty = transaction
            key_prefix = "fish" if item_type == "f" else "bugs"
        elif type(transaction) is str:
            key_prefix, item_id, qty = "fossils", transaction, 1
        else:
            raise IOError

        key = key_prefix + str(item_id)
        # try not locking cost_dict since these are idempotent writes, we may run a few extra network calls
        if key in cost_dict:
            outputs[index] = cost_dict[key] * qty
        else:
        # network call slow, memoize and parallelize
            thread = threading.Thread(target=process_transaction, args=(key_prefix, item_id, index, qty, outputs))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    return sum(outputs)


def process_line(line: str, top_lines: List[Tuple[str, int]], user_expenditure: Dict[str, int]):
    user_id, transactions = json.loads(line)
    transaction_cost = cost_of_transactions(transactions)
    # print(transaction_cost)

    # Add to line computation
    transaction_tuple = (line, transaction_cost)
    with line_lock:
        if len(top_lines) < 5:
            top_lines.append(transaction_tuple)
        else:
            # stable comparison
            if transaction_cost > top_lines[-1][1]:
                top_lines[-1] = transaction_tuple
        # Sort
        top_lines.sort(key=lambda x: x[1], reverse=True)

    with user_lock:
        past_expenditure = user_expenditure.get(user_id, 0)
        user_expenditure[user_id] = transaction_cost + past_expenditure


def multi_threaded_impl(filename: str, max_lines: int = None, max_threads: int = 10) -> Tuple[Any, Any]:
    cost_dict.clear()
    global network_calls
    network_calls = 0
    start_time = time()
    # for largest sales and biggest user spenders, some sort of heap?
    # no need for heap, tree etc. since the constant number (top 5)
    # limits runtime to linear time
    user_expenditure: Dict[str, int] = {}
    top_lines: List[Tuple[str, int]] = []

    threads = []

    with open(filename, 'r') as f:
        # lazy load, assume individual lines fit in memory
        # seems reasonable since with 16GB of ram, which
        # is reasonable for PCs, 10GB is approximately 1B transactions
        # (10 bytes per transaction) -- biggest sale of all time
        # and definitely does not fit in inventory :)
        for n_line, line in enumerate(f):
            if max_lines is not None and n_line >= max_lines:
                break

            thread = threading.Thread(target=process_line, args=(line, top_lines, user_expenditure))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    top_users: List[Tuple[str, int]] = []
    for user_id, spend in user_expenditure.items():
        user_spend_tuple = (user_id, spend)
        if len(top_users) < 5:
            top_users.append(user_spend_tuple)
        else:
            # stable comparison
            if spend > top_users[-1][1]:
                top_users[-1] = user_spend_tuple
        # Sort
        top_users = sorted(top_users, key=lambda x: x[1], reverse=True)

    # print("Top 5 transactions:\n")
    # for line, transaction in top_lines:
    #     print(line, "(" + str(transaction) + ")")
    #
    # print("\nTop 5 users by sales:\n")
    # for user_id, spend in top_users:
    #     print(user_id, "(" + str(spend) + ")")

    end_time = time()
    print("Total time taken:", end_time - start_time, "seconds for", n_line + 1, "lines")

    return top_lines, top_users
