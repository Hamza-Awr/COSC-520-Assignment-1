import unittest
import random
import string
from data_structures.Hash import HashTable

# helper benchmark for HashTable (same style as others)
def benchmark_hash(n):
    chars = string.ascii_lowercase + string.digits
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    ht = HashTable(size=2 * n)
    for name in usernames:
        ht.insert(name)

    # Lookup set: half present, half absent
    lookups = min(1000 // 2, len(usernames))
    negatives = 1000 - lookups

    lookup_names = random.sample(usernames, lookups)
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(negatives)]

    import time
    start = time.perf_counter_ns()
    for name in lookup_names:
        ht.contains(name)
    total_time = time.perf_counter_ns() - start
    return (total_time / len(lookup_names)) / 1e9


class TestHashTable(unittest.TestCase):

    def setUp(self):
        """Prepare a hash table with random usernames."""
        self.chars = string.ascii_lowercase + string.digits
        self.n = 2000
        self.ht = HashTable(size=2 * self.n)

        self.usernames = [''.join(random.choice(self.chars) for _ in range(5)) + str(i) for i in range(self.n)]
        for u in self.usernames:
            self.ht.insert(u)

        self.target_exists = self.usernames[1000]
        self.target_absent = ''.join(random.choice(self.chars) for _ in range(8))

    def test_found(self): # testing usernames that exist
        result = self.ht.contains(self.target_exists)
        print(f"\nHashTable existing username: {self.target_exists} → {result}")
        self.assertTrue(result)

    def test_not_found(self): # testing usernames that don't exist
        result = self.ht.contains(self.target_absent)
        print(f"\nHashTable absent username: {self.target_absent} → {result}")
        self.assertFalse(result)

    def test_benchmark_small(self): # testing small amount of usernames
        n = 2000
        t = benchmark_hash(n)
        print(f"\nBenchmark HashTable with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

    def test_benchmark_large(self): # testing large amount of usernames
        n = 20000
        t = benchmark_hash(n)
        print(f"\nBenchmark HashTable with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
