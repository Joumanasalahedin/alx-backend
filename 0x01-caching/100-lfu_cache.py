#!/usr/bin/env python3
"""LFU Cache - Task 5"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache inherits from BaseCaching and implements an LFU caching system.
    When the cache exceeds the MAX_ITEMS limit,
    the least frequently used items are discarded.
    If there is a tie, the least recently used item is discarded.
    """

    def __init__(self):
        """
        Initialize the class by calling the parent constructor.
        """
        super().__init__()
        self.usage_frequency = {}
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache.
        If key or item is None, this method should not do anything.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.usage_frequency[key] += 1
                self.order.remove(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    min_freq = min(self.usage_frequency.values())
                    lfu_keys = [
                        k for k in self.usage_frequency if self.usage_frequency[k] == min_freq]
                    if len(lfu_keys) > 1:
                        lfu_key = next(k for k in self.order if k in lfu_keys)
                    else:
                        lfu_key = lfu_keys[0]
                    del self.cache_data[lfu_key]
                    del self.usage_frequency[lfu_key]
                    self.order.remove(lfu_key)
                    print(f"DISCARD: {lfu_key}")
                self.cache_data[key] = item
                self.usage_frequency[key] = 1
            self.order.append(key)

    def get(self, key):
        """
        Get an item by key.
        If key is None or if the key doesn’t exist, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        self.usage_frequency[key] += 1
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data.get(key)
