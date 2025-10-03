# Import necessary libraries
from random import choice, sample
from string import ascii_lowercase, digits
import matplotlib.pyplot as plt
import time

chars = ascii_lowercase + digits # random usernames
n_list_linear = [10**3, 10**4, 10**5, 10**6, 10**7]   # The list of n's (number of usernames) we will search through
times_linear = []

for n in n_list_linear:
    # generate random usernames
    usernames = [''.join(choice(chars) for _ in range(5)) + str(i) for i in range(n)]
    
    number = 1000 # Number of usernames you want to search
    lookups = min(number//2, len(usernames)) # number will either be half OR the total length of the usernames
    negative_samples = number - lookups # number of usernames to search NOT present (some usernames to search won't be present, and it doesn't matter, we just want to search)

    lookup_names = []
    lookup_names.extend(sample(usernames, lookups)) # the usernames to search
    lookup_names.extend([''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]) # adding the names not present

    start_time = time.perf_counter_ns() # start recording time
    for name in lookup_names:
        for u in usernames:   # linear search through lookup_names
            if u == name:
                break # when found, break
    total_time = time.perf_counter_ns() - start_time # end time of search of total names

    avg_time_sec = (total_time / len(lookup_names)) / 1e9 # divide total time by no. of usernames to find the average lookup time in seconds
    times_linear.append(avg_time_sec) # append it to the list of times for each n

    print(f"n={n}, average lookup time={avg_time_sec:.8f} s")

# Plot the graph of n vs time
plt.plot(n_list_linear, times_linear, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Number of usernames (n)")
plt.ylabel("Average lookup time (s)")
plt.title("Linear Search Average Lookup Performance")
plt.show()