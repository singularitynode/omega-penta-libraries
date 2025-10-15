# 🚀 Omega Penta Libraries

**Enterprise-Grade Distributed Systems Libraries for Python**

## 📦 The 5 Omega Libraries

### 1. `omega_domain.querycache` - Automatic Data Mesh
- **Problem Solved**: Slow complex queries across multiple microservices
- **Features**: Query Federation, Distributed Caching, Field-level Resolution

### 2. `omega_infra.gate` - Distributed Rate Limiter  
- **Problem Solved**: Manual rate limiting without global view
- **Features**: Token Bucket Algorithm, Distributed Consensus, Dynamic Throttling

### 3. `omega_infra.circuitbreaker` - Adaptive Protection
- **Problem Solved**: Cascading failures in microservices
- **Features**: State Machine (OPEN/HALF_OPEN/CLOSED), Self-healing, Production-ready

### 4. `omega_domain.snapshotter` - Aggregate Root Persistence
- **Problem Solved**: Event Sourcing performance issues
- **Features**: State Snapshots, Event Replay Optimization, Auto-snapshotting

### 5. `omega_infra.shard` - Consistent Hashing Router
- **Problem Solved**: Data routing with minimal rebalancing
- **Features**: Consistent Hashing, Virtual Nodes, Scalable Sharding

## 🚀 Quick Start

```python
# Install dependencies
pip install redis asyncio

# Basic usage example
from omega_infra.circuitbreaker import CircuitBreaker

circuit_breaker = CircuitBreaker("payment_gateway")

@circuit_breaker.protect
async def call_external_service():
    return await your_api_call()
