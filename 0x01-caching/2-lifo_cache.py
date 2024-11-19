#!/usr/bin/env python3
"""LIFO Cache"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache inherits from BaseCaching and implements a LIFO caching system.
    When the cache exceeds the MAX_ITEMS limit,
    the most recently added items are discarded.
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
        If key or item is None, this method should not do anything.
        If the number of items exceeds MAX_ITEMS,
        the most recently added item must be discarded.
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # LIFO behavior: remove the most recently added key
                    last_key = self.order.pop()
                    del self.cache_data[last_key]
                    print(f"DISCARD: {last_key}")
                self.order.append(key)
            else:
                # Update the order if the key already exists
                self.order.remove(key)
                self.order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key.
        If key is None or if the key doesn’t exist, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
