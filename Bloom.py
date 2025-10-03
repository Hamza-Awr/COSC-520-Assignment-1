import mmh3, time, random
from string import ascii_lowercase, digits
from bitarray import bitarray
import matplotlib.pyplot as plt
import numpy as np

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


chars = ascii_lowercase + digits
n_list_bloom = [10**3, 10**4, 10**5, 10**6, 10**7]  # list of username numbers to check 
times_bloom = []

for n in n_list_bloom:
    # Generate usernames
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    # Create Bloom filter
    bf = BloomFilter(size=n*10, hash_count=5)

    # Add all usernames
    for name in usernames:
        bf.add(name)

    number = 1000 # Number of usernames you want to search
    lookups = min(number//2, len(usernames)) # number will either be half OR the total length of the usernames
    negative_samples = number - lookups # number of usernames to search NOT present (some usernames to search won't be present, and it doesn't matter, we just want to search)

    lookup_names = []
    lookup_names.extend(sample(usernames, lookups)) # the usernames to search
    lookup_names.extend([''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]) # adding the names not present

    # Time lookups
    start = time.perf_counter_ns()
    for u in lookup_names:
        _ = bf.check(u)
    end = time.perf_counter_ns()

    avg_time = ((end - start) / number) / 1e9 # Find average time of a lookup
    times_bloom.append(avg_time)

    print(f"n={n}, avg lookup time={avg_time:.9f} s (sampled {number} usernames)")

# Plot Results of times taken to search an entry using a Bloom Filter
plt.plot(n_list_bloom, times_bloom, marker="o", label="Bloom Filter Lookup")
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Number of usernames (n)")
plt.ylabel("Avg lookup time (s)")
plt.title("Bloom Filter Average Lookup Time vs n (mmh3)")
plt.legend()
plt.show()