import unittest
import random
import string
from data_structures.Binary_search import binary_search, benchmark_binary_search

class TestBinarySearch(unittest.TestCase):

    def setUp(self):
        """Prepare a sorted dataset for binary search."""
        self.chars = string.ascii_lowercase + string.digits
        self.usernames = sorted([''.join(random.choice(self.chars) for _ in range(5)) + str(i) for i in range(2000)])
        self.target_exists = self.usernames[1000]
        self.target_absent = ''.join(random.choice(self.chars) for _ in range(8))

    def test_found(self):
        result = binary_search(self.usernames, self.target_exists)
        print(f"\nBinary Search existing username: {self.target_exists} → {result}")
        self.assertTrue(result)

    def test_not_found(self):
        result = binary_search(self.usernames, self.target_absent)
        print(f"\nBinary Search absent username: {self.target_absent} → {result}")
        self.assertFalse(result)

    def test_benchmark_small(self):
        n = 2000
        t = benchmark_binary_search(n)
        print(f"\nBenchmark Binary Search with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

    def test_benchmark_large(self):
        n = 20000
        t = benchmark_binary_search(n)
        print(f"\nBenchmark Binary Search with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
