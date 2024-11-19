#!/usr/bin/python3
"""FIFO Cache"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache inherits from BaseCaching and
    implements a FIFO caching system.
    When the cache exceeds the MAX_ITEMS limit,
    the first added items are discarded.
    """
    def __init__(self):
        """
        Initialize the class by calling the parent constructor.
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache.
        If key or item is None, should not do anything.
        If the number of items exceeds MAX_ITEMS,
        the first item must be discarded.
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    first_key = self.order.pop(0)
                    del self.cache_data[first_key]
                    print(f"DISCARD: {first_key}")
                self.order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key.
        If key is None or if key doesn’t exist, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
