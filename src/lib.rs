use pyo3::prelude::*;
use ::heavykeeper::TopK;
use std::collections::HashMap;

/// A Python wrapper for the HeavyKeeper algorithm
/// 
/// HeavyKeeper is a sketch-based algorithm for finding the top-K most frequent
/// items in a data stream with high accuracy and low memory usage.
#[pyclass]
pub struct HeavyKeeper {
    inner: TopK<String>,
}

#[pymethods]
impl HeavyKeeper {
    /// Create a new HeavyKeeper instance
    /// 
    /// Args:
    ///     k: The number of top items to track
    ///     width: The width of the sketch (number of buckets)
    ///     depth: The depth of the sketch (number of hash functions)
    ///     decay: The decay factor for aging items (between 0.0 and 1.0)
    /// 
    /// Returns:
    ///     A new HeavyKeeper instance
    #[new]
    fn new(k: usize, width: usize, depth: usize, decay: f64) -> PyResult<Self> {
        let inner = TopK::new(k, width, depth, decay);
        Ok(HeavyKeeper { inner })
    }
    
    /// Add an item to the sketch
    /// 
    /// Args:
    ///     item: The string item to add
    /// 
    /// Returns:
    ///     None
    fn add(&mut self, item: &str) {
        self.inner.add(&item.to_string());
    }
    
    /// Add multiple items efficiently (batch operation)
    fn add_bulk(&mut self, items: Vec<String>) {
        for item in items {
            self.inner.add(&item);
        }
    }
    
    /// Check if an item is being tracked in the top-K list
    /// 
    /// Args:
    ///     item: The string item to query
    /// 
    /// Returns:
    ///     True if the item is being tracked
    fn query(&self, item: &str) -> bool {
        self.inner.query(&item.to_string())
    }
    
    /// Get the estimated count for an item
    /// 
    /// Args:
    ///     item: The string item to query
    /// 
    /// Returns:
    ///     The estimated count for the item (0 if not tracked)
    fn count(&self, item: &str) -> u64 {
        self.inner.count(&item.to_string())
    }
    
    /// Get the top-K items and their counts as a dictionary
    /// 
    /// Returns:
    ///     A dictionary mapping items to their estimated counts
    fn get_topk(&self) -> PyResult<HashMap<String, u64>> {
        let nodes = self.inner.list();
        let mut result = HashMap::new();
        
        for node in nodes {
            result.insert(node.item, node.count);
        }
        
        Ok(result)
    }
    
    /// Get the top-K items as a list of tuples
    /// 
    /// Returns:
    ///     A list of (item, count) tuples sorted by count in descending order
    fn list(&self) -> PyResult<Vec<(String, u64)>> {
        let nodes = self.inner.list();
        let result: Vec<(String, u64)> = nodes
            .into_iter()
            .map(|node| (node.item, node.count))
            .collect();
        
        Ok(result)
    }
    
    /// Get the current number of items being tracked
    /// 
    /// Returns:
    ///     The number of items in the top-K list
    fn len(&self) -> usize {
        self.inner.list().len()
    }
    
    /// Check if the sketch is empty
    /// 
    /// Returns:
    ///     True if no items are being tracked
    fn is_empty(&self) -> bool {
        self.inner.list().is_empty()
    }

    /// Support for Python's built-in len() function
    fn __len__(&self) -> usize {
        self.inner.list().len()
    }
}

/// Python module for HeavyKeeper algorithm
#[pymodule]
fn heavykeeper(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<HeavyKeeper>()?;
    m.add("__version__", "0.1.0")?;
    Ok(())
} 
