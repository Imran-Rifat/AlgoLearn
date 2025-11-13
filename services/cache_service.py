import redis
import json
import os
from typing import Any, Optional


class CacheService:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.ttl = 86400  # 24 hours in seconds
        self._client = None

    @property
    def client(self):
        """Lazy initialization of Redis client"""
        if self._client is None:
            try:
                self._client = redis.Redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                self._client.ping()
            except:
                # Fallback to in-memory cache if Redis is unavailable
                self._client = None
                self._memory_cache = {}
        return self._client

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.client:
                value = self.client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Fallback to memory cache
                return self._memory_cache.get(key)
        except:
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        try:
            serialized_value = json.dumps(value)
            if self.client:
                return self.client.set(key, serialized_value, ex=ttl or self.ttl)
            else:
                # Fallback to memory cache
                self._memory_cache[key] = value
                return True
        except:
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self.client:
                return bool(self.client.delete(key))
            else:
                # Fallback to memory cache
                if key in self._memory_cache:
                    del self._memory_cache[key]
                    return True
                return False
        except:
            return False

    def clear_pattern(self, pattern: str) -> int:
        """Clear keys matching pattern"""
        try:
            if self.client:
                keys = self.client.keys(pattern)
                if keys:
                    return self.client.delete(*keys)
            else:
                # Fallback to memory cache
                keys_to_delete = [k for k in self._memory_cache.keys() if pattern in k]
                for key in keys_to_delete:
                    del self._memory_cache[key]
                return len(keys_to_delete)
        except:
            return 0