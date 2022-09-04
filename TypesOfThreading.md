# Short note on threading

## What is threading?

A process can spin up threads (light-weight process)
 which share heap memory (dynamically allocated) but not stack memory.
 
Spinning up threads is useful for concurrent execution in the face of IO blocking.
Ex: while waiting for network calls, keyboard input, etc.

The general idea is that you can have multiple threads (streams of execution) that
run, not in parallel, but rather while other threads are waiting/have nothing to do.

In other words, we make sure to maximally utilize CPU, and gains are
from using the CPU at all times rather than parallelism, which would require
additional CPUs.

### Should I use a process instead?
If you don't need to share memory, you can use multiple processes instead.

### Is there any downside to having multiple threads run concurrently?
You'll have to use mutual exclusion on shared memory as multiple threads
 could attempt to modify this shared data. Since operations like
  increments (read-write) are not atomic, these could lead to data races.
 
This can lead to complexity and make it challenging to reason about your
 program's correctness. You also need to be careful that the latency introduced
 by threads waiting for synchronization primitives like locks does not outweigh
 the benefit from concurrent execution.
 

### How is threading complicated by computer architecture?

To obtain performance optimizations, CPUs use various <a href="https://en.wikipedia.org/wiki/Out-of-order_execution">out of order execution</a>
(OOO) techniques. An individual CPU is not allowed to do so in a way that reorders program instructions, ie breaks program correctness.

In short, there aren't any challenges on a single CPU from OOO, although data races remain an issue (hence the need for mutual exclusion primitives).

However, on multi-core systems, multiple CPUs running threads from the same program
are unaware of other CPUs' memory accesses and so are unaware of any memory
access reordering they perform. In this situation, memory barriers/memory fences
are necessary, which have the effect of synchronizing memory state across all CPUs<a href="https://stackoverflow.com/questions/59217821/why-memory-reordering-is-not-a-problem-on-single-core-processor-machines">[1]</a>.

### Does multi-threading scale?

As the number of concurrent threads increases and contention increases, lock-free
data structures become a means of squeezing out performance improvements. Since mutexes
serve as memory barriers, lock-free alternatives that also serve as memory barriers ex: atomics need to be used.