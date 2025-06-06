# heavykeeper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Python bindings for the HeavyKeeper algorithm - a fast, memory-efficient sketch-based algorithm for finding the top-K most frequent items in data streams.

## Overview

HeavyKeeper is a probabilistic data structure that identifies the most frequent items in a data stream using minimal memory. This implementation provides Python bindings for a high-performance Rust implementation of the algorithm.

### Key Features

- 🚀 **High Performance**: Rust-based implementation with Python bindings via PyO3
- 💾 **Memory Efficient**: Uses probabilistic sketching to track millions of items with minimal memory
- 🎯 **Top-K Tracking**: Efficiently maintains the K most frequent items
- 🔄 **Stream Processing**: Designed for continuous data streams
- 📊 **Approximate Counts**: Provides estimated frequencies with high accuracy
- 🧪 **Battle Tested**: Includes comprehensive benchmarks and tests

### Use Cases

- **Log Analysis**: Find the most frequent IP addresses, user agents, or error messages
- **Text Processing**: Identify the most common words in large documents
- **Network Monitoring**: Track heavy hitters in network traffic
- **Clickstream Analysis**: Find the most popular pages or user actions
- **Time Series Data**: Monitor frequently occurring events or anomalies

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/pmcgleen/heavykeeper-py.git
cd heavykeeper-py

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Build and install the Python package
maturin develop

# Or build a wheel
maturin build --release
```

### Requirements

- Python 3.11+
- Rust toolchain (for building from source)

## Quick Start

```python
from heavykeeper import HeavyKeeper

# Create a HeavyKeeper instance
# k=100: track top 100 items
# width=2048: sketch width (affects accuracy)
# depth=8: number of hash functions (affects accuracy)
# decay=0.9: aging factor for old items
hk = HeavyKeeper(k=100, width=2048, depth=8, decay=0.9)

# Add items to the stream
items = ["apple", "banana", "apple", "cherry", "apple", "banana"]
for item in items:
    hk.add(item)

# Query individual items
print(f"Is 'apple' in top-K? {hk.query('apple')}")
print(f"Estimated count for 'apple': {hk.count('apple')}")

# Get all top-K items
top_items = hk.list()  # Returns list of (item, count) tuples
print("Top items:", top_items)

# Get as dictionary
top_dict = hk.get_topk()  # Returns {item: count} dictionary
print("Top items dict:", top_dict)
```

## API Reference

### `HeavyKeeper(k, width, depth, decay)`

Creates a new HeavyKeeper instance.

**Parameters:**
- `k` (int): Number of top items to track
- `width` (int): Width of the sketch (number of buckets)
- `depth` (int): Depth of the sketch (number of hash functions)  
- `decay` (float): Decay factor for aging items (between 0.0 and 1.0)

### Methods

#### `add(item: str) -> None`
Add an item to the sketch.

#### `query(item: str) -> bool`
Check if an item is being tracked in the top-K list.

#### `count(item: str) -> int`
Get the estimated count for an item (returns 0 if not tracked).

#### `list() -> List[Tuple[str, int]]`
Get the top-K items as a list of (item, count) tuples, sorted by count.

#### `get_topk() -> Dict[str, int]`  
Get the top-K items as a dictionary mapping items to counts.

#### `len() -> int`
Get the current number of items being tracked.

#### `is_empty() -> bool`
Check if the sketch is empty.

## Benchmarking

The repository includes several benchmark scripts for performance testing:

### Word Count Benchmark

```bash
# Basic benchmark with a text file
python benchmark_wordcount.py -k 100 -f your_text_file.txt --time

# Using different parsing methods
python benchmark_wordcount.py -k 100 -f large_file.txt --method mmap --time

# Custom parameters
python benchmark_wordcount.py -k 50 -w 4096 -d 4 -y 0.8 -f data.txt --time
```

## Parameter Tuning

### Choosing Parameters

- **k**: Set to the number of top items you need
- **width**: Larger values improve accuracy but use more memory (try 1024-8192)
- **depth**: More hash functions improve accuracy (try 4-16)  
- **decay**: Controls how quickly old items are forgotten (0.8-0.99)

### Memory Usage

Approximate memory usage: `width × depth × 16 bytes + k × (item_size + 16 bytes)`

For typical usage (width=2048, depth=8, k=100):
- Sketch: ~262 KB
- Top-K storage: ~depends on item sizes

### Accuracy vs Performance

- Higher `width` and `depth` → better accuracy, more memory
- Lower `decay` → faster adaptation to changes, less stability
- Higher `k` → more items tracked, slightly more overhead

## Development

### Building

```bash
# Development build
maturin develop

# Release build  
maturin build --release

# Build with debugging
maturin develop --debug
```

### Testing

```bash
# Run the test suite
python test_heavykeeper.py

# Run benchmarks
python benchmark_wordcount.py -k 10 -f test_file.txt
```

### Project Structure

```
heavykeeper-py/
├── src/
│   └── lib.rs          # Rust implementation and Python bindings
├── benchmark_*.py      # Performance benchmarks
├── test_heavykeeper.py # Test suite
├── Cargo.toml          # Rust dependencies
├── pyproject.toml      # Python package configuration
└── README.md           # This file
```

## Algorithm Details

HeavyKeeper uses a sketch-based approach with the following components:

1. **Count-Min Sketch**: Probabilistic counting structure
2. **Heavy Part**: Stores the actual top-K items
3. **Exponential Decay**: Ages out old items over time
4. **Hash Functions**: Multiple hash functions for better accuracy

The algorithm provides strong theoretical guarantees while maintaining excellent practical performance.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on the HeavyKeeper algorithm research
- Built with [PyO3](https://pyo3.rs/) for Rust-Python interoperability
- Uses [Maturin](https://github.com/PyO3/maturin) for building Python extensions
