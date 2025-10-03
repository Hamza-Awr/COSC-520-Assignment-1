# COSC 520 – Assignment 1

This repository contains Python implementations and benchmarks for five different search and lookup data structures and algorithms:

- **Linear Search**
- **Binary Search**
- **Hash Table**
- **Bloom Filter**
- **Cuckoo Filter**

Each data structure has:
- An implementation file inside the `data_structures/` folder
- A corresponding test file inside the `tests/` folder

## Project Structure
```
COSC-520-Assignment-1/
│
├── data_structures/
│ ├── Linear_search.py
│ ├── Binary_search.py
│ ├── Hash.py
│ ├── Bloom.py
│ └── Cuckoo.py
│
├── tests/
│ ├── test_linear_search.py
│ ├── test_binary_search.py
│ ├── test_hash.py
│ ├── test_bloom.py
│ └── test_cuckoo.py
│
├── plots/ # contains plots of individual and combined time complexities of different data structures (for lookup)
│
├── README.md # (this file)
└── requirements.txt # (dependencies if needed)
```

1. Clone this repository
   ```bash
   git clone https://github.com/Hamza-Awr/COSC-520-Assignment-1.git
   cd COSC-520-Assignment-1
   ```

2. (Optional but recommended) Create a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate     # macOS/Linux
    venv\Scripts\activate        # Windows
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Running the Implementations

Each implementation can be run directly for benchmarking.
For example:

```bash
python data_structures/Linear_search.py
```

This will execute the script’s benchmarking function and plot the lookup time complexity for that data structure/algorithm.

## Running Unit Tests
### Run individual test files

```bash
python -m unittest tests/test_linear_search.py -v
python -m unittest tests/test_binary_search.py -v
python -m unittest tests/test_hash.py -v
python -m unittest tests/test_bloom.py -v
python -m unittest tests/test_cuckoo.py -v
```

### Run all tests at once
From the root folder:

```bash
python -m unittest discover -v tests
```
The -v flag enables verbose mode, showing which test is running and the result.

## Notes

- The maximum tested input size was 10 million due to memory and time limitations, instead of the suggested 1 billion. This is justified because the time plots still reflect the correct theoretical time complexities.
- Only lookup times were measured.
- Plots can be generated from the notebook or scripts where implemented.

## Example Test Output

Running all tests:

```bash
python -m unittest discover -v tests
```

Output:
```bash
test_benchmark_large (test_binary_search.TestBinarySearch) ... 
Benchmark Binary Search with n=20000 → avg lookup time=1.925300e-06 seconds
ok
test_benchmark_small (test_binary_search.TestBinarySearch) ...
Benchmark Binary Search with n=2000 → avg lookup time=1.461200e-06 seconds
ok
test_found (test_binary_search.TestBinarySearch) ...
Binary Search existing username: iqgjo764 → True
ok
test_not_found (test_binary_search.TestBinarySearch) ...
Binary Search absent username: nv89i79c → False
ok
test_benchmark_large (test_bloom.TestBloomFilter) ...
Benchmark Bloom Filter with n=20000 → avg lookup time=1.531500e-06 seconds
ok
...
----------------------------------------------------------------------
Ran 20 tests in 0.699s

OK
```
