import unittest
import random
import string
from data_structures.Linear_search import linear_search, benchmark_linear_search

class TestLinearSearch(unittest.TestCase):

    def setUp(self):
        """Prepare a larger test dataset once for all tests."""
        self.chars = string.ascii_lowercase + string.digits
        self.usernames = [''.join(random.choice(self.chars) for _ in range(5)) + str(i) for i in range(1000)]
        # pick a target that exists
        self.target_exists = self.usernames[500]
        # random target that doesn’t exist
        self.target_absent = ''.join(random.choice(self.chars) for _ in range(8))

    def test_found(self): # testing usernames that exist
        result = linear_search(self.usernames, self.target_exists)
        print(f"\nSearching for existing username: {self.target_exists} → {result}")
        self.assertTrue(result)

    def test_not_found(self): # testing usernames that don't exist
        result = linear_search(self.usernames, self.target_absent)
        print(f"\nSearching for absent username: {self.target_absent} → {result}")
        self.assertFalse(result)

    def test_benchmark_small(self): # testing small amount of usernames
        n = 1000
        t = benchmark_linear_search(n)
        print(f"\nBenchmark Linear Search with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

    def test_benchmark_large(self): # testing large amount of usernames
        n = 10000
        t = benchmark_linear_search(n)
        print(f"\nBenchmark Linear Search with n={n} → avg lookup time={t:.6e} seconds")
        self.assertGreater(t, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
