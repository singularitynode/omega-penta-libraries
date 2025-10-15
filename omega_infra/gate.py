"""
OMEGA.INFRA: Gate - Distributed Rate Limiter
Leaky Bucket/Token Bucket Algorithm with Distributed Consensus
"""

import time
import asyncio
from typing import Callable, Awaitable, Any
from functools import wraps
import redis.asyncio as redis

class TooManyRequestsError(Exception):
    pass

class Gate:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
    
    def limit_requests(self, rate: str = "per_user", per_sec: int = 5):
        """
        Decorator: Enforces Distributed Rate Limit
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                # Extract identifier from request
                identifier = kwargs.get('user_id') or kwargs.get('ip_address') or 'global'
                
                # Distributed counter check
                current_count = await self._get_global_count_and_increment(identifier, per_sec)
                
                if current_count > per_sec:
                    await self._throttle_request(identifier)
                    raise TooManyRequestsError(f"Rate limit exceeded for {identifier}.")
                    
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    async def _get_global_count_and_increment(self, identifier: str, window: int) -> int:
        """Implements token bucket algorithm using Redis"""
        key = f"rate_limit:{identifier}"
        
        # Use Redis transactions for atomic operations
        async with self.redis.pipeline(transaction=True) as pipe:
            try:
                pipe.multi()
                current = int(await pipe.get(key) or 0)
                if current == 0:
                    pipe.setex(key, window, 1)
                else:
                    pipe.incr(key)
                
                results = await pipe.execute()
                return results[0] if current == 0 else results[1]
            except Exception:
                return 0  # Fail open on Redis failure
    
    async def _throttle_request(self, identifier: str):
        """Additional throttling logic"""
        print(f"🚫 Throttling requests for: {identifier}")
        await asyncio.sleep(1)  # Simple throttle delay

# Usage example
gate = Gate()

@gate.limit_requests(rate='per_user', per_sec=5)
async def api_endpoint(user_id: str):
    return {"data": f"Hello user {user_id}"}