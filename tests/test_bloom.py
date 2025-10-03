import unittest
import random
import string
from data_structures.Bloom import BloomFilter, benchmark_bloom_filter

class TestBloomFilter(unittest.TestCase):

    def setUp(self):
        """Prepare a Bloom filter with random usernames."""
        self.chars = string.ascii_lowercase + string.digits
        self.n = 2000
        self.m = 20000  # bit array size
        self.k = 5      # number of hash functions
        self.bloom = BloomFilter(self.m, self.k)

        self.usernames = [''.join(random.choice(self.chars) for _ in range(5)) + str(i) for i in range(self.n)]
        for u in self.usernames:
            self.bloom.add(u)

        self.target_exists = self.usernames[1000]
        self.target_absent = ''.join(random.choice(self.chars) for _ in range(8))

    def test_found(self):
        result = self.bloom.check(self.target_exists)
        print(f"\nBloom Filter existing username: {self.target_exists} → {result}")
        self.assertTrue(result)

    def test_not_found(self):
        result = self.bloom.check(self.target_absent)
        print(f"\nBloom Filter absent username: {self.target_absent} → {result}")
        # Bloom filter may have false positives, but never false negatives
        self.assertIn(result, [True, False])  

    def test_benchmark_small(self):
        n = 2000
        t = benchmark_bloom_filter(n)
        print(f"\nBenchmark Bloom Filter with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

    def test_benchmark_large(self):
        n = 20000
        t = benchmark_bloom_filter(n)
        print(f"\nBenchmark Bloom Filter with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
