import mmh3
from bitarray import bitarray
from random import choice, sample
from string import ascii_lowercase, digits

# Using MurmurHash3 for both hashing functions
class BloomFilter:
    def __init__(self, size=1000000, hash_count=5):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        # mmh3 returns 32-bit signed int, take abs to avoid negatives
        return [(abs(mmh3.hash(item, i)) % self.size) for i in range(self.hash_count)]

    # inserting a username
    def add(self, item):
        for index in self._hashes(item):
            self.bit_array[index] = 1

    # checking if a username exists
    def check(self, item):
        return all(self.bit_array[index] for index in self._hashes(item))

def benchmark_bloom_filter(n, number=1000):
    chars = ascii_lowercase + digits
    usernames = [''.join(choice(chars) for _ in range(5)) + str(i) for i in range(n)]
    bf = BloomFilter(size=n*10, hash_count=5)

    for name in usernames:
        bf.add(name)

    lookups = min(number//2, len(usernames)) # same strategy for every algorithm/data structure
    negative_samples = number - lookups
    lookup_names = sample(usernames, lookups) + [''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]

    import time
    start = time.perf_counter_ns()
    for u in lookup_names:
        _ = bf.check(u)
    end = time.perf_counter_ns()

    avg_time_sec = ((end - start) / len(lookup_names)) / 1e9
    return avg_time_sec

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    n_list_bloom = [10**3, 10**4, 10**5, 10**6, 10**7] # number of usernames (n)
    times_bloom = []

    for n in n_list_bloom:
        avg_time = benchmark_bloom_filter(n)
        times_bloom.append(avg_time)
        print(f"n={n}, avg lookup time={avg_time:.9f} s")

    plt.plot(n_list_bloom, times_bloom, marker="o", color='red', label="Bloom Filter Lookup")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Avg lookup time (s)")
    plt.title("Bloom Filter Average Lookup Time Performance")
    plt.legend()
    plt.show()
