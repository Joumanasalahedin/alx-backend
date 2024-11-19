#!/usr/bin/env python3
"""LRU Cache - Task 3"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache inherits from BaseCaching and implements a LRU caching system.
    When the cache exceeds the MAX_ITEMS limit,
    the least recently used items are discarded.
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
        the least recently used item must be discarded.
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    lru_key = self.order.pop(0)
                    del self.cache_data[lru_key]
                    print(f"DISCARD: {lru_key}")
            else:
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
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data.get(key)
