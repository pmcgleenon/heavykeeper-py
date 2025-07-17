#!/usr/bin/env python3
"""
Benchmark script for HeavyKeeper word counting.
"""

import argparse
import time
import sys
from pathlib import Path
from heavykeeper import HeavyKeeper


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Benchmark HeavyKeeper word counting')
    parser.add_argument('-k', '--topk', type=int, default=100, 
                       help='Number of top items to track (default: 100)')
    parser.add_argument('-w', '--width', type=int, default=2048,
                       help='Sketch width (default: 2048)')
    parser.add_argument('-d', '--depth', type=int, default=8,
                       help='Sketch depth (default: 8)')
    parser.add_argument('-y', '--decay', type=float, default=0.9,
                       help='Decay factor (default: 0.9)')
    parser.add_argument('-f', '--file', required=True,
                       help='Input text file')
    parser.add_argument('--method', choices=['read', 'mmap'], default='read',
                       help='File reading method (default: read)')
    parser.add_argument('--time', action='store_true',
                       help='Show timing information')
    return parser.parse_args()


def read_file_content(file_path, method='read'):
    """Read file content using specified method."""
    if method == 'mmap':
        import mmap
        with open(file_path, 'r', encoding='utf-8') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                return mm.read().decode('utf-8')
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def extract_words(text):
    """Extract words from text, simple implementation."""
    import re
    # Simple word extraction - split on whitespace and filter
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words


def benchmark_wordcount(args):
    """Run the word count benchmark."""
    # Check if file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1
    
    # Create HeavyKeeper instance
    hk = HeavyKeeper(k=args.topk, width=args.width, depth=args.depth, decay=args.decay)
    
    # Read file
    start_time = time.time()
    content = read_file_content(file_path, args.method)
    read_time = time.time() - start_time
    
    # Extract words
    start_time = time.time()
    words = extract_words(content)
    extract_time = time.time() - start_time
    
    # Process words with HeavyKeeper
    start_time = time.time()
    for word in words:
        hk.add(word)
    process_time = time.time() - start_time
    
    # Get results
    start_time = time.time()
    top_items = hk.list()
    result_time = time.time() - start_time
    
    # Print results
    print(f"Processed {len(words)} words from '{args.file}'")
    print()
    print(f"Top {len(hk)} items:")
    for i, (word, count) in enumerate(top_items[:20], 1):  # Show top 20
        print(f"  {i:2d}. {word}: {count}")
    
    if len(top_items) > 20:
        print(f"  ... and {len(top_items) - 20} more items")
    
    # Print timing if requested
    if args.time:
        print()
        print("Timing information:")
        print(f"  File read:     {read_time:.4f}s")
        print(f"  Word extract:  {extract_time:.4f}s")
        print(f"  Processing:    {process_time:.4f}s")
        print(f"  Result fetch:  {result_time:.4f}s")
        print(f"  Total:         {read_time + extract_time + process_time + result_time:.4f}s")
    
    return 0


def main():
    """Main entry point."""
    args = parse_args()
    try:
        return benchmark_wordcount(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 