# MLM Commission Engine

This project is a high-performance daily commission calculation engine for a multilevel marketing (MLM) network.

## Features

- **High-Performance Calculation**: Utilizes a `O(n)` algorithm (post-order DFS with memoization) to calculate commissions efficiently.
- **Scalable**: Designed to handle networks of 50,000+ partners with deep hierarchies (15+ levels).
- **Accurate Commission Logic**: Calculates a 5% commission on the gross profit from all descendants in a partner's downline.
- **Flexible Date Handling**: Supports commission calculations for any given month, correctly handling variable month lengths (including leap years).
- **Robust Error Handling**: Includes validation for input data, detection of cycles in the hierarchy, and handling of missing parent references.
- **CLI Interface**: A user-friendly command-line interface for running the commission engine.
- **Comprehensive Test Suite**: Includes unit and integration tests with `pytest` to ensure correctness and reliability.
- **Benchmarking Tools**: Comes with scripts to generate large datasets and benchmark the engine's performance against the specified targets.

## Project Structure

```
mlm_commission_engine/
├── main.py                 # CLI entry point
├── src/
│   ├── __init__.py
│   ├── commission_engine.py    # Core algorithm
│   ├── data_loader.py         # JSON I/O handling
│   ├── tree_validator.py      # Cycle detection
│   └── utils.py              # Helper functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_commission_engine.py
│   ├── test_data_loader.py
│   ├── test_tree_validator.py
│   └── test_integration.py
├── benchmarks/
│   ├── benchmark.py          # Performance testing
│   └── generate_test_data.py # Large dataset generator
├── README.md                 # Detailed documentation
├── requirements.txt          # Dependencies (minimal)
└── sample_data/
    └── partners.json         # Test dataset
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd mlm_commission_engine
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Commission Engine

To calculate commissions, run the `main.py` script with the required arguments.

```bash
python main.py --input /path/to/partners.json --output /path/to/commissions.json [--month YYYY-MM]
```

- `--input`: Path to the input JSON file containing partner data.
- `--output`: Path where the output JSON file with commissions will be saved.
- `--month` (optional): The month for the calculation in `YYYY-MM` format. If omitted, the current month is used.

**Example:**

```bash
python main.py --input sample_data/partners.json --output commissions.json --month 2023-11
```

### Running Tests

The project includes a comprehensive test suite. To run the tests, use `pytest`:

```bash
pytest
```

### Benchmarking

To test the performance of the engine, you first need to generate a large dataset and then run the benchmark script.

1.  **Generate a large test file (e.g., 50,000 partners):**

    ```bash
    python benchmarks/generate_test_data.py --num-partners 50000 --output sample_data/large_partners.json
    ```

2.  **Run the benchmark script:**
    ```bash
    python benchmarks/benchmark.py --input sample_data/large_partners.json
    ```

## Algorithm Choice Justification

The core of this engine is a recursive algorithm that traverses the partner hierarchy. The chosen approach is a **post-order Depth-First Search (DFS) with memoization**.

### Post-Order DFS with Memoization

- **How it works**: This algorithm works by traversing the hierarchy tree down to the leaf nodes and then calculating total revenue upwards. For any given partner, it first recursively calculates the total revenue for all of their children's downlines. The total revenue for a partner is the sum of their own monthly revenue plus the total revenues of their children's entire downlines.
- **Memoization**: To avoid redundant calculations, the total downline revenue for each partner is stored (memoized) the first time it is computed. On subsequent requests, the cached value is returned instantly.

### Time and Space Complexity

- **Time Complexity: `O(n)`**: Where `n` is the number of partners. Thanks to memoization, each partner's downline revenue is calculated exactly once. The entire process involves a single pass over the hierarchy.
- **Space Complexity: `O(n)`**: The space is required for:
  1.  Storing the partner data in a dictionary for `O(1)` lookups.
  2.  The adjacency list representation of the tree.
  3.  The memoization cache, which stores the calculated revenue for each partner.
  4.  The recursion stack, which in a balanced tree is `O(log n)` but could be `O(n)` in the worst case (a single long chain).

### Alternative Considered: Bottom-Up Dynamic Programming

A bottom-up iterative approach was considered. This would involve identifying all leaf nodes and then processing the tree level by level, from the bottom up.

- **Comparison**: A post-order DFS with memoization is functionally equivalent to a topological sort combined with dynamic programming on a Directed Acyclic Graph (DAG), which is what a hierarchy tree is. The recursive DFS approach is often more intuitive to implement for tree-like structures and naturally handles the post-order traversal without needing to explicitly manage levels or queues of nodes. The performance characteristics are identical (`O(n)` time, `O(n)` space), making the recursive DFS a clean and efficient choice.

## Performance

The engine is designed to meet the target of processing **50,000 partners in under 2 seconds**. The `benchmarks/benchmark.py` script can be used to validate this on your hardware. The chosen algorithm is highly efficient and should meet this target on the specified hardware (4-core 3.0GHz CPU, 8GB RAM).
