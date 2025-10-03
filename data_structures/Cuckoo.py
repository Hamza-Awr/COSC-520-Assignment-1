import hashlib, random
from string import ascii_lowercase, digits
from random import sample

# Cuckoo Filter 
class CuckooFilter:
    def __init__(self, bucket_count=10000, bucket_size=2, max_kicks=500):
        # Number of buckets in the filter
        self.bucket_count = bucket_count
        # Number of fingerprint slots per bucket
        self.bucket_size = bucket_size
        # Max number of evictions allowed when inserting
        self.max_kicks = max_kicks
        # Initialize buckets as empty lists
        self.buckets = [[] for _ in range(bucket_count)]

    def _fingerprint(self, item):
        # Create a short fingerprint of the item (fixed-size string)
        # Using SHA-256 then truncating to 32 hex chars
        h = hashlib.sha256(item.encode()).hexdigest()
        return h[:32]

    def _hashes(self, fp):
        # Compute two candidate bucket indices for a fingerprint
        h1 = int(hashlib.sha256(fp.encode()).hexdigest(), 16) % self.bucket_count
        h2 = (h1 ^ int(hashlib.sha256(fp.encode()).hexdigest(), 16)) % self.bucket_count
        return h1, h2

    def insert(self, item):
        # Insert an item by placing its fingerprint into one of two buckets
        fp = self._fingerprint(item)
        i1, i2 = self._hashes(fp)

        # Try direct insert in either candidate bucket
        for i in [i1, i2]:
            if len(self.buckets[i]) < self.bucket_size:
                self.buckets[i].append(fp)
                return True

        # If both are full, perform "kicks" (evictions)
        i = random.choice([i1, i2])
        for _ in range(self.max_kicks):
            j = random.randint(0, self.bucket_size - 1)
            fp, self.buckets[i][j] = self.buckets[i][j], fp

            i1, i2 = self._hashes(fp)
            i = i2 if i == i1 else i1

            if len(self.buckets[i]) < self.bucket_size:
                self.buckets[i].append(fp)
                return True

        return False

    # Check if the item exists in the cuckoo filter
    def lookup(self, item):
        fp = self._fingerprint(item)
        i1, i2 = self._hashes(fp)
        return fp in self.buckets[i1] or fp in self.buckets[i2]

# Testing the lookup times of different number of usernames
def benchmark_cuckoo_filter(n, number=1000):
    chars = ascii_lowercase + digits # random username
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)] # Generate random usernames 
    cf = CuckooFilter(bucket_count=n*2, bucket_size=4) # Make a cuckoo filter object

    for name in usernames:
        cf.insert(name)

    lookups = min(number//2, len(usernames))
    negative_samples = number - lookups
    lookup_names = sample(usernames, lookups) + [''.join(random.choice(chars) for _ in range(5)) for _ in range(negative_samples)]

    import time
    start = time.perf_counter_ns()
    for name in lookup_names:
        cf.lookup(name)
    end = time.perf_counter_ns()
    avg_time_sec = ((end - start) / len(lookup_names)) / 1e9
    return avg_time_sec

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    n_list_cuckoo = [10**3, 10**4, 10**5, 10**6, 10**7]
    times_cuckoo = []

    for n in n_list_cuckoo:
        avg_time = benchmark_cuckoo_filter(n)
        times_cuckoo.append(avg_time)
        print(f"n={n}, avg lookup time={avg_time:.9f} s")

    plt.plot(n_list_cuckoo, times_cuckoo, marker="o", color="blue", label="Cuckoo Filter Lookup")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average lookup time (s)")
    plt.title("Cuckoo Filter Average Lookup Performance")
    plt.legend()
    plt.show()
