Goal: given a file containing a list of user transactions, process each transaction by fetching price from ACNH API,
 compute transaction price, and return top transactions and users

Compute:
- Process lines in parallel so as to run network calls concurrently.
    - Need to lock prices data structure for mutual exclusion;
    however, pricing calls are idempotent so we don't actually need to lock, although we'll run a few extra network calls.
    -
- Cache results of network calls.

Storage:

BW:


Raw notes:
- Adding in a shared counter to track network calls was expensive
- Removing locking of prices data structures improves performance
- On avg. network calls take 0.06-0.12s to run


Future ideas:
- Use condition variables
- Explore Queues for inter-thread messaging
    - The above two ideas come from https://google.github.io/styleguide/pyguide.html#Threading
- Retries or self rate-limiting to circumvent server-side rate-limiting
- Multiprocessing to break down computation further?
- Lock-free tracking of top_users/lines
- Concurrency for the network calls per transaction
- Connection reuse, congestion window control, etc. improvement
- Database storage

Completed ideas:
- ~~Verify correctness (compare single and multi-threaded output across 3 runs)~~
