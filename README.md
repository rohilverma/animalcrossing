# animalcrossing
An exploration of theory and practical limits of threading + processing using Animal Crossing New Horizons

The basic problem is to process a .csv of transactions, fetch prices for the goods in each transaction, and compute the largest transactions & biggest spenders.

I wanted to see how fast this could be done in Python, making use of optimizations such as threading, multicore processing, and connection reuse.

## Summary of files
1. Design.md: A number of different ideas/observations on how to make this code more efficient
2. TypesOfThreading.md: A short note on different types of threading designs, including complications brought on by compiler out-of-order execution.
3. *.py: Code to verify correctness of multithreaded implementations, to compare different multithreaded implementations, to compare threads vs. processes for Python (and come face to face with the GIL!), and to compare the utility of different connection reusing designs.
4. Storage/ : Folder to store state, ex: expected output
5. Pastes/ : Timing data from various profiling runs.
