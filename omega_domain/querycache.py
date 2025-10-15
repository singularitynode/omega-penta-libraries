"""
OMEGA.DOMAIN: QueryCache - Automatic Data Mesh
Federated query execution with distributed caching
"""

import asyncio
from typing import Dict, Any, List
import redis.asyncio as redis

class QueryCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.service_mapping = {
            'user_profile': 'http://user-service/api',
            'inventory': 'http://inventory-service/api', 
            'order_history': 'http://order-service/api'
        }
    
    async def fetch_federated_data(self, query_fields: List[str], entity_id: str) -> Dict[str, Any]:
        """
        Automatically constructs final data object by calling
        multiple microservices (Data Mesh) and caching each field
        """
        final_data = {"id": entity_id}
        
        # 1. FIELD-LEVEL RESOLUTION & CACHING
        for field in query_fields:
            service_name = self._map_field_to_service(field)
            cache_key = f"{service_name}:{entity_id}:{field}"

            # 2. PROXY CALL with caching
            field_data = await self._get_from_cache_or_service(cache_key, service_name, entity_id, field)
            final_data[field] = field_data
            
        return final_data
    
    def _map_field_to_service(self, field: str) -> str:
        """Maps field names to appropriate microservices"""
        field_service_map = {
            'name': 'user_profile',
            'email': 'user_profile',
            'inventory_count': 'inventory',
            'last_order_date': 'order_history'
        }
        return field_service_map.get(field, 'user_profile')
    
    async def _get_from_cache_or_service(self, cache_key: str, service_name: str, entity_id: str, field: str) -> Any:
        """Gets data from cache or calls the actual service"""
        # Try cache first
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return cached_data.decode()
        
        # If not in cache, call service (simulated)
        service_data = await self._call_service(service_name, entity_id, field)
        
        # Cache for 5 minutes
        await self.redis.setex(cache_key, 300, str(service_data))
        return service_data
    
    async def _call_service(self, service_name: str, entity_id: str, field: str) -> str:
        """Simulates calling a microservice"""
        await asyncio.sleep(0.1)  # Simulate network delay
        return f"mock_data_{field}_{entity_id}"

# Usage example
async def example_usage():
    cache = QueryCache()
    profile = await cache.fetch_federated_data(
        ['name', 'inventory_count', 'last_order_date'], 
        'user-123'
    )
    print(profile)