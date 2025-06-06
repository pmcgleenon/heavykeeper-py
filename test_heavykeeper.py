#!/usr/bin/env python3

from heavykeeper import HeavyKeeper

def test_basic_functionality():
    """Test basic HeavyKeeper functionality."""
    print("Testing HeavyKeeper Python bindings...")
    
    # Create a HeavyKeeper instance
    hk = HeavyKeeper(k=5, width=1024, depth=4, decay=0.9)
    
    # Add some test words
    test_words = [
        "hello", "world", "hello", "python", "rust",
        "hello", "world", "programming", "hello", "test",
        "hello", "world", "hello", "coding", "hello"
    ]
    
    print(f"Adding {len(test_words)} words...")
    for word in test_words:
        hk.add(word)
    
    print(f"Total unique items tracked: {len(hk)}")
    print(f"Is empty: {hk.is_empty()}")
    
    # Test query functionality
    print(f"\nQuery results:")
    for word in ["hello", "world", "python", "nonexistent"]:
        is_tracked = hk.query(word)
        count = hk.count(word)
        print(f"  {word}: tracked={is_tracked}, count={count}")
    
    # Get top-k as list
    print(f"\nTop-K items (as list):")
    for word, count in hk.list():
        print(f"  {word}: {count}")
    
    # Get top-k as dictionary
    print(f"\nTop-K items (as dict):")
    topk_dict = hk.get_topk()
    for word, count in sorted(topk_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"  {word}: {count}")

def test_with_file():
    """Test with a simple text file."""
    import tempfile
    import os
    
    # Create a temporary file with test content
    test_content = """
    The quick brown fox jumps over the lazy dog.
    The dog was lazy, but the fox was quick and brown.
    Quick brown foxes are better than lazy dogs.
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        print(f"\nTesting with file: {temp_file}")
        
        # Run the benchmark script
        import subprocess
        result = subprocess.run([
            'python3', 'benchmark_wordcount.py', 
            '-k', '10', 
            '-f', temp_file,
            '--time'
        ], capture_output=True, text=True)
        
        print("Benchmark output:")
        print(result.stdout)
        if result.stderr:
            print("Timing info:")
            print(result.stderr)
            
    finally:
        # Clean up
        os.unlink(temp_file)

if __name__ == "__main__":
    test_basic_functionality()
    test_with_file() 