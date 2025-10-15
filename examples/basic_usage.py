"""
Basic usage examples for all 5 Omega libraries
"""

import asyncio
from omega_domain.querycache import QueryCache
from omega_infra.gate import Gate, TooManyRequestsError
from omega_infra.circuitbreaker import CircuitBreaker, CircuitOpenError
from omega_domain.snapshotter import Snapshotter
from omega_infra.shard import Shard

async def demo_query_cache():
    """Demo the QueryCache library"""
    print("🔍 Testing QueryCache...")
    cache = QueryCache()
    result = await cache.fetch_federated_data(
        ['name', 'inventory_count'], 
        'user-123'
    )
    print(f"QueryCache Result: {result}")

async def demo_gate():
    """Demo the Gate rate limiter"""
    print("🚦 Testing Gate Rate Limiter...")
    gate = Gate()
    
    @gate.limit_requests(per_sec=2)
    async def limited_function(user_id: str):
        return f"Processed {user_id}"
    
    try:
        for i in range(5):
            result = await limited_function(user_id=f"user-{i}")
            print(f"Request {i}: {result}")
            await asyncio.sleep(0.1)
    except TooManyRequestsError as e:
        print(f"Rate limited: {e}")

async def demo_circuit_breaker():
    """Demo the CircuitBreaker"""
    print("⚡ Testing CircuitBreaker...")
    cb = CircuitBreaker("demo_service", max_failures=2)
    
    @cb.protect
    async def unreliable_service():
        # Simulate occasional failures
        import random
        if random.random() > 0.5:
            raise Exception("Service temporarily unavailable")
        return "Service response"
    
    for i in range(5):
        try:
            result = await unreliable_service()
            print(f"Call {i}: {result}")
        except (CircuitOpenError, Exception) as e:
            print(f"Call {i}: Failed - {e}")
        await asyncio.sleep(0.5)

def demo_shard():
    """Demo the Shard router"""
    print("🔗 Testing Shard Router...")
    shard = Shard(['node-a', 'node-b', 'node-c'])
    
    test_keys = ['user-100', 'user-200', 'user-300']
    for key in test_keys:
        node = shard.get_node(key)
        print(f"Key '{key}' → Node '{node}'")

async def main():
    """Run all demos"""
    await demo_query_cache()
    print()
    
    await demo_gate() 
    print()
    
    await demo_circuit_breaker()
    print()
    
    demo_shard()

if __name__ == "__main__":
    asyncio.run(main())