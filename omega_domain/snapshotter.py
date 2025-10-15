"""
OMEGA.DOMAIN: Snapshotter - Aggregate Root Persistence
Optimizes Event Sourcing performance with state snapshots
"""

import json
import asyncio
from typing import Dict, Any, List
import redis.asyncio as redis

class Snapshotter:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.snapshot_threshold = 10  # Events before snapshot
    
    async def load_aggregate_state(self, aggregate_id: str) -> Dict[str, Any]:
        """
        Loads Aggregate Root state from latest Snapshot
        Only replays events since last snapshot
        """
        # 1. Load Latest Snapshot
        snapshot_key = f"snapshot:{aggregate_id}"
        snapshot_data = await self.redis.get(snapshot_key)
        
        if snapshot_data:
            state = json.loads(snapshot_data)
            last_version = state.get('_version', 0)
        else:
            state = {}
            last_version = 0
        
        # 2. Replay Recent Events
        events = await self._fetch_events_since(aggregate_id, last_version)
        current_state = self._apply_events(state, events)
        
        # 3. AUTO-SNAPSHOT if needed
        if len(events) >= self.snapshot_threshold:
            await self._save_snapshot(aggregate_id, current_state, last_version + len(events))
        
        return current_state
    
    async def _fetch_events_since(self, aggregate_id: str, version: int) -> List[Dict]:
        """Fetch events after specified version"""
        events_key = f"events:{aggregate_id}"
        all_events = await self.redis.lrange(events_key, version, -1)
        return [json.loads(event) for event in all_events]
    
    def _apply_events(self, state: Dict, events: List[Dict]) -> Dict:
        """Apply events to rebuild state"""
        for event in events:
            event_type = event.get('type')
            if event_type == 'USER_CREATED':
                state.update(event['data'])
            elif event_type == 'USER_UPDATED':
                state.update(event['data'])
            # Add more event types as needed
        
        state['_version'] = len(events)
        return state
    
    async def _save_snapshot(self, aggregate_id: str, state: Dict, version: int):
        """Save current state as snapshot"""
        snapshot_key = f"snapshot:{aggregate_id}"
        state['_version'] = version
        state['_snapshot_time'] = asyncio.get_event_loop().time()
        
        await self.redis.setex(
            snapshot_key, 
            3600,  # 1 hour TTL
            json.dumps(state)
        )
        print(f"📸 Saved snapshot for {aggregate_id} at version {version}")

# Usage example
async def example_snapshot_usage():
    snapshotter = Snapshotter()
    
    # Load user state efficiently
    user_state = await snapshotter.load_aggregate_state("user-123")
    print(f"User state: {user_state}")