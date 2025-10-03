import mmh3
from random import choice, sample
from string import ascii_lowercase, digits

# Simple hash table using MurmurHash3 + chaining
# Using MurmurHash3 for hashing. It is non-cryptographic so it's faster and security is not needed for this assignment's purpose.
# Tried SHA-256 but it was taking too long
class HashTable:
    def __init__(self, size=10**6):
        # Initialize table with empty lists for chaining
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        # Compute hash index using MurmurHash3
        return mmh3.hash(key) % self.size

    def insert(self, key):
        # Insert key if not already present in the chain
        idx = self._hash(key)
        if key not in self.table[idx]:
            self.table[idx].append(key)

    def contains(self, key):
        # Check if key exists in the hash table
        idx = self._hash(key)
        return key in self.table[idx]

def benchmark_hash_table(n, number=1000):
    """
    Build hash table of n usernames and perform lookups
    """
    chars = ascii_lowercase + digits
    usernames = [''.join(choice(chars) for _ in range(5)) + str(i) for i in range(n)]
    ht = HashTable(size=2*n)

    for name in usernames:
        ht.insert(name)

    lookups = min(number//2, len(usernames))
    negative_samples = number - lookups
    lookup_names = sample(usernames, lookups) + [''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]

    import time
    start_time = time.perf_counter_ns()
    for name in lookup_names:
        ht.contains(name)
    total_time = time.perf_counter_ns() - start_time
    avg_time_sec = (total_time / len(lookup_names)) / 1e9
    return avg_time_sec

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    n_list_hash = [10**3, 10**4, 10**5, 10**6, 10**7]
    times_hash = []

    for n in n_list_hash:
        avg_time = benchmark_hash_table(n)
        times_hash.append(avg_time)
        print(f"n={n}, avg lookup time={avg_time:.9f} s")

    plt.plot(n_list_hash, times_hash, marker='o', color='green')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average lookup time (s)")
    plt.title("Custom Hash Table (MurmurHash3) Lookup Performance")
    plt.show()
