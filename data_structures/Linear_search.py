# Import necessary libraries
from random import choice, sample
from string import ascii_lowercase, digits

chars = ascii_lowercase + digits # random usernames

def linear_search(lst, target):
    """
    Simple linear search: returns True if target is in lst
    """
    for item in lst:
        if item == target:
            return True # when found, break
    return False

def benchmark_linear_search(n, number=1000):
    """
    Generate 'n' usernames, perform 'number' lookups (half existing, half random that may not be present within the list)
    Returns average lookup time in seconds
    number = Number of usernames you want to search
    """
    usernames = [''.join(choice(chars) for _ in range(5)) + str(i) for i in range(n)] # generate random usernames
    lookups = min(number//2, len(usernames)) #  number will either be half OR the total length of the usernames
    negative_samples = number - lookups # number of usernames to search NOT present (some usernames to search won't be present, and it doesn't matter, we just want to search)

    lookup_names = sample(usernames, lookups) + [''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]

    import time
    start_time = time.perf_counter_ns() # start recording time
    for name in lookup_names: # linear search through lookup_names
        linear_search(usernames, name)
    total_time = time.perf_counter_ns() - start_time # end time of search of total names
    avg_time_sec = (total_time / len(lookup_names)) / 1e9 # divide total time by no. of usernames to find the average lookup time in seconds
    return avg_time_sec 

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    n_list_linear = [10**3, 10**4, 10**5, 10**6, 10**7]
    times_linear = []

    for n in n_list_linear:
        avg_time = benchmark_linear_search(n)
        times_linear.append(avg_time)
        print(f"n={n}, average lookup time={avg_time:.8f} s")
    
    # Plot the graph of n vs time
    plt.plot(n_list_linear, times_linear, marker='o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average lookup time (s)")
    plt.title("Linear Search Average Lookup Performance")
    plt.show()
