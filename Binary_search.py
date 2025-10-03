# Import necessary libraries
from random import choice, sample
from string import ascii_lowercase, digits
import matplotlib.pyplot as plt
import time

chars = ascii_lowercase + digits # random usernames
n_list_binary = [10**3, 10**4, 10**5, 10**6, 10**7]   # The list of n's (number of usernames) we will search through
times_binary = []

def binary_search(sorted_list, target):
    """
    Binary search function. Does the same as bisect.bisect_left.
    Goes to the middle of an array, sees if target is on the left or right (or middle), and bisects it continuously until the target is found
    """
    left, right = 0, len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return True
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

for n in n_list_binary:
    # Generate usernames
    usernames = [''.join(choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    usernames.sort()  # sorting is required for binary search

    number = 1000 # Number of usernames you want to search
    lookups = min(number//2, len(usernames)) # number will either be half OR the total length of the usernames
    negative_samples = number - lookups # number of usernames to search NOT present (some usernames to search won't be present, and it doesn't matter, we just want to search)

    lookup_names = []
    lookup_names.extend(sample(usernames, lookups)) # the usernames to search
    lookup_names.extend([''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]) # adding the names not present

    # Time multiple lookups
    start_time = time.perf_counter_ns()
    for name in lookup_names:
        binary_search(usernames, name)
    total_time = time.perf_counter_ns() - start_time

    avg_time_sec = (total_time / len(lookup_names)) / 1e9 # divide total time by no. of usernames to find the average lookup time in seconds
    times_binary.append(avg_time_sec)

    print(f"n={n}, avg lookup time={avg_time_sec:.9f} s")

# Plot the graph of n vs time
plt.plot(n_list_binary, times_binary, marker='o', color='orange')
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of usernames (n)")
plt.ylabel("Average lookup time (s)")
plt.title("Binary Search Average Lookup Performance")
plt.show()
