# ⚡ Omega Penta Libraries  
**Enterprise-Grade Distributed Systems Toolkit for Python**

[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![Stars](https://img.shields.io/github/stars/singularitynode/omega-penta-libraries?style=social)]()

---

## 🧩 The 5 Core Libraries

### 1. `omega_domain.querycache` — Intelligent Data Mesh
**Solves:** Cross-service query latency  
**Features:**
- Query federation with zero boilerplate  
- Distributed field-level caching  
- Auto-invalidates on domain event updates  

---

### 2. `omega_infra.gate` — Distributed Rate Limiter  
**Solves:** Manual rate limiting without global visibility  
**Features:**
- Token Bucket + Consensus coordination  
- Dynamic throttling  
- Redis or in-memory backend  

---

### 3. `omega_infra.circuitbreaker` — Adaptive Circuit Protection  
**Solves:** Cascading microservice failures  
**Features:**
- State machine (OPEN / HALF_OPEN / CLOSED)  
- Failure decay with sliding window metrics  
- Async-safe and production-hardened  

---

### 4. `omega_domain.snapshotter` — High-Performance Event Snapshotting  
**Solves:** Slow event replay and persistence  
**Features:**
- Aggregate state snapshots  
- Event replay optimization  
- Auto-snapshot based on delta threshold  

---

### 5. `omega_infra.shard` — Scalable Consistent Hashing Router  
**Solves:** Painful data rebalancing during scaling  
**Features:**
- Virtual node hashing  
- Deterministic routing  
- Fault-tolerant shard reassignment  

---

## 🚀 Quick Start

```bash
pip install redis asyncio
python
Copy code
from omega_infra.circuitbreaker import CircuitBreaker

cb = CircuitBreaker("payment_gateway")

@cb.protect
async def call_api():
    return await external_call()
🧠 Advanced Capabilities
Feature	Description	Supported
🕸 Cluster Awareness	Works across distributed nodes	✅
🧮 Adaptive Thresholds	Learns optimal break thresholds over time	✅
💾 Persistent Caching	Redis + local disk hybrid cache	✅
🧱 Pluggable Backends	Swap transport layers (Kafka, NATS, HTTP)	✅
🔮 Predictive Heuristics	ML-assisted service degradation prediction	🚧 (In Dev)

🧩 Architecture Overview
text
Copy code
 ┌────────────────────────────┐
 │     Omega Penta Layer     │
 │ ┌────────────────────────┐│
 │ │  ω-domain (logic)      ││
 │ │  ω-infra (infrastructure)││
 │ └────────────────────────┘│
 └───────────▲────────────────┘
             │
     AsyncIO / Redis / Thread-Safe IO
Each module is designed with quantum-inspired modularity — isolated, yet interconnected through a common async event bus.

⚖️ Comparison
Library	Core Strength	Distributed Safe	Async	Auto-Recovery
Omega Penta	Multi-layer, cluster-aware	✅	✅	✅
ResilientLib	Basic retry wrappers	❌	⚠️	❌
Tenacity	Retry-based	❌	✅	❌
CircuitBreakerPy	Single-node	⚠️	✅	⚠️

🧰 Use Cases
Fintech transaction throttling

Distributed caching systems

Event-sourced architecture

Resilient microservice coordination

🧾 License
MIT License © 2025 singularitynode

⭐ Contribute & Support
If this library saved you hours — give it a star!
Contributions, ideas, and issue reports are welcome.

"Built for systems that never sleep." — Omega Core Design Team

