#!/usr/bin/env python3

import pytest
import tempfile
import os
import subprocess
from heavykeeper import HeavyKeeper


def test_basic_functionality():
    """Test basic HeavyKeeper functionality."""
    # Create a HeavyKeeper instance
    hk = HeavyKeeper(k=5, width=1024, depth=4, decay=0.9)
    
    # Add some test words
    test_words = [
        "hello", "world", "hello", "python", "rust",
        "hello", "world", "programming", "hello", "test",
        "hello", "world", "hello", "coding", "hello"
    ]
    
    # Add all words (using default increment of 1)
    for word in test_words:
        hk.add(word)
    
    # Test basic properties
    assert len(hk) > 0, "HeavyKeeper should track some items"
    assert not hk.is_empty(), "HeavyKeeper should not be empty after adding items"
    
    # Test query functionality
    assert hk.query("hello"), "Should track 'hello'"
    assert hk.query("world"), "Should track 'world'"
    assert hk.query("python"), "Should track 'python'"
    assert not hk.query("nonexistent"), "Should not track 'nonexistent'"
    
    # Test count functionality
    assert hk.count("hello") > 0, "Should have count for 'hello'"
    assert hk.count("world") > 0, "Should have count for 'world'"
    assert hk.count("python") > 0, "Should have count for 'python'"
    assert hk.count("nonexistent") == 0, "Should have zero count for 'nonexistent'"
    
    # Test that hello has higher count than python (since it appears more)
    assert hk.count("hello") > hk.count("python"), "More frequent word should have higher count"
    
    # Test list functionality
    topk_list = hk.list()
    assert len(topk_list) > 0, "Should return some items from list()"
    assert all(isinstance(item, tuple) and len(item) == 2 for item in topk_list), "List items should be tuples of (word, count)"
    
    # Test get_topk functionality
    topk_dict = hk.get_topk()
    assert len(topk_dict) > 0, "Should return some items from get_topk()"
    assert all(isinstance(count, (int, float)) for count in topk_dict.values()), "Counts should be numeric"


def test_empty_heavykeeper():
    """Test HeavyKeeper behavior when empty."""
    hk = HeavyKeeper(k=5, width=1024, depth=4, decay=0.9)
    
    assert hk.is_empty(), "New HeavyKeeper should be empty"
    assert len(hk) == 0, "New HeavyKeeper should have length 0"
    assert not hk.query("any"), "Empty HeavyKeeper should not track any items"
    assert hk.count("any") == 0, "Empty HeavyKeeper should return 0 for any count"
    assert len(hk.list()) == 0, "Empty HeavyKeeper should return empty list"
    assert len(hk.get_topk()) == 0, "Empty HeavyKeeper should return empty dict"


def test_heavykeeper_parameters():
    """Test HeavyKeeper with different parameters."""
    # Test with different k values
    hk1 = HeavyKeeper(k=3, width=512, depth=3, decay=0.8)
    hk2 = HeavyKeeper(k=10, width=2048, depth=5, decay=0.95)
    
    # Add same data to both
    test_words = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    for word in test_words:
        hk1.add(word)
        hk2.add(word)
    
    # Both should track items
    assert not hk1.is_empty()
    assert not hk2.is_empty()
    
    # Both should return some results
    assert len(hk1.list()) > 0
    assert len(hk2.list()) > 0


def test_heavykeeper_increments():
    """Test HeavyKeeper with custom increments."""
    hk = HeavyKeeper(k=5, width=1024, depth=4, decay=0.9)

    # Add items with different increments
    hk.add("item1", 1)    # Default increment
    hk.add("item2", 5)    # Custom increment
    hk.add("item3", 10)   # Larger increment
    hk.add("item1", 2)    # Add to existing item

    # Test that counts reflect the increments
    assert hk.count("item1") >= 3, "item1 should have count >= 3 (1+2)"
    assert hk.count("item2") >= 5, "item2 should have count >= 5"
    assert hk.count("item3") >= 10, "item3 should have count >= 10"

    # Test bulk add with custom increment
    hk.add_bulk(["bulk1", "bulk2", "bulk3"], 7)
    assert hk.count("bulk1") >= 7, "bulk1 should have count >= 7"
    assert hk.count("bulk2") >= 7, "bulk2 should have count >= 7"
    assert hk.count("bulk3") >= 7, "bulk3 should have count >= 7"


def test_heavykeeper_with_seed():
    """Test HeavyKeeper with deterministic seed."""
    # Create two instances with the same seed
    hk1 = HeavyKeeper.with_seed(k=5, width=1024, depth=4, decay=0.9, seed=42)
    hk2 = HeavyKeeper.with_seed(k=5, width=1024, depth=4, decay=0.9, seed=42)

    # Add same data to both
    test_words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in test_words:
        hk1.add(word, 1)
        hk2.add(word, 1)

    # Results should be identical (due to same seed)
    list1 = hk1.list()
    list2 = hk2.list()

    assert len(list1) == len(list2), "Both instances should track same number of items"

    # Convert to dictionaries for easier comparison
    dict1 = {item: count for item, count in list1}
    dict2 = {item: count for item, count in list2}

    assert dict1 == dict2, "Results should be identical with same seed"


def test_heavykeeper_edge_cases():
    """Test edge cases and error conditions."""
    # Test with empty string
    hk = HeavyKeeper(k=5, width=1024, depth=4, decay=0.9)
    hk.add("")
    assert hk.query(""), "Should track empty string"
    assert hk.count("") > 0, "Should have count for empty string"

    # Test with very long string
    long_string = "a" * 1000
    hk.add(long_string)
    assert hk.query(long_string), "Should track long string"
    assert hk.count(long_string) > 0, "Should have count for long string"

    # Test with special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    hk.add(special_chars)
    assert hk.query(special_chars), "Should track special characters"
    assert hk.count(special_chars) > 0, "Should have count for special characters"


if __name__ == "__main__":
    pytest.main([__file__]) 