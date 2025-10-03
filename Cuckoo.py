# import necessary libraries
import hashlib, random, time
from string import ascii_lowercase, digits
import matplotlib.pyplot as plt
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
        # Using SHA-256 then truncating to 8 hex chars
        # (Not secure, but fine for demonstration)
        h = hashlib.sha256(item.encode()).hexdigest()
        return h[:8]

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
            # Evict a random fingerprint from bucket i
            j = random.randint(0, self.bucket_size - 1)
            fp, self.buckets[i][j] = self.buckets[i][j], fp  # swap the content of the two buckets

            # Compute alternate index for evicted fingerprint
            i1, i2 = self._hashes(fp)
            i = i2 if i == i1 else i1

            # Try to place evicted fingerprint in alternate bucket
            if len(self.buckets[i]) < self.bucket_size:
                self.buckets[i].append(fp)
                return True

        # If insertion fails after max_kicks, filter is full
        return False

    def lookup(self, item):
        # Lookup checks if fingerprint exists in either candidate bucket
        fp = self._fingerprint(item)
        i1, i2 = self._hashes(fp)
        return fp in self.buckets[i1] or fp in self.buckets[i2]

chars = ascii_lowercase + digits
n_list_cuckoo = [10**3, 10**4, 10**5, 10**6]   # test different sizes of n (number of usernames)
times_cuckoo = []  # store average lookup times

for n in n_list_cuckoo:
    # Generate n usernames (random 5 chars + unique index)
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    # Initialize Cuckoo Filter with 2n buckets and 4 slots each
    cf = CuckooFilter(bucket_count=n*2, bucket_size=4)

    # Insert usernames into the filter
    for name in usernames:
        cf.insert(name)

    # Build lookup test set (half positive, half negative)
    number = 1000  # fixed lookup count
    lookups = min(number//2, len(usernames))       # positive (present) lookups
    negative_samples = number - lookups            # negative (not present) lookups

    lookup_names = []
    lookup_names.extend(sample(usernames, lookups))  # sample existing usernames
    lookup_names.extend([''.join(random.choice(chars) for _ in range(5)) for _ in range(negative_samples)])  # random new

    # Time the lookups
    start = time.perf_counter_ns()
    for name in lookup_names:
        cf.lookup(name)
    total_time = time.perf_counter_ns() - start

    # Compute average lookup time in seconds for one search
    avg_time_sec = (total_time / len(lookup_names)) / 1e9
    times_cuckoo.append(avg_time_sec)

    print(f"n={n}, avg lookup time={avg_time_sec:.9f} s")

# Plot Results of n vs. time
plt.plot(n_list_cuckoo, times_cuckoo, marker="o", color="blue", label="Cuckoo Filter Lookup")
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Number of usernames (n)")
plt.ylabel("Average lookup time (s)")
plt.title("Cuckoo Filter Average Lookup Performance")
plt.legend()
plt.show()