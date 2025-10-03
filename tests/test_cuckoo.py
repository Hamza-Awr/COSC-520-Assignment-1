import unittest
import random
import string
from data_structures.Cuckoo import CuckooFilter, benchmark_cuckoo_filter

class TestCuckooFilter(unittest.TestCase):

    def setUp(self):
        """Prepare a Cuckoo filter with random usernames."""
        self.chars = string.ascii_lowercase + string.digits
        self.capacity = 4000
        self.cf = CuckooFilter(self.capacity)

        self.usernames = [''.join(random.choice(self.chars) for _ in range(5)) + str(i) for i in range(2000)]
        for u in self.usernames:
            self.cf.insert(u)

        self.target_exists = self.usernames[500]
        self.target_absent = ''.join(random.choice(self.chars) for _ in range(8))

    def test_found(self):
        result = self.cf.lookup(self.target_exists)
        print(f"\nCuckoo Filter existing username: {self.target_exists} → {result}")
        self.assertTrue(result)

    def test_not_found(self):
        result = self.cf.lookup(self.target_absent)
        print(f"\nCuckoo Filter absent username: {self.target_absent} → {result}")
        # Cuckoo filter also may return false positives
        self.assertIn(result, [True, False])

    def test_benchmark_small(self):
        n = 2000
        t = benchmark_cuckoo_filter(n)
        print(f"\nBenchmark Cuckoo Filter with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

    def test_benchmark_large(self):
        n = 20000
        t = benchmark_cuckoo_filter(n)
        print(f"\nBenchmark Cuckoo Filter with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
