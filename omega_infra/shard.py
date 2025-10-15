"""
OMEGA.INFRA: Shard - Consistent Hashing Router
Minimal data movement when scaling database/cache instances
"""

import hashlib
from typing import List, Any

class Shard:
    def __init__(self, nodes: List[str] = None, virtual_nodes: int = 150):
        self.nodes = nodes or ['db-node-1', 'db-node-2', 'db-node-3']
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self._build_ring()
    
    def _build_ring(self):
        """Build the consistent hashing ring with virtual nodes"""
        for node in self.nodes:
            for i in range(self.virtual_nodes):
                virtual_node = f"{node}-vnode-{i}"
                key = self._hash(virtual_node)
                self.ring[key] = node
    
    def _hash(self, key: str) -> int:
        """Generate consistent hash for key"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def get_node(self, key: str) -> str:
        """
        Automatically computes the correct node for a key using
        Consistent Hashing, minimizing data movement when nodes change
        """
        if not self.ring:
            return self.nodes[0]  # Fallback
        
        key_hash = self._hash(key)
        sorted_keys = sorted(self.ring.keys())
        
        # Find the first node with hash >= key_hash
        for ring_key in sorted_keys:
            if ring_key >= key_hash:
                return self.ring[ring_key]
        
        # Wrap around to first node
        return self.ring[sorted_keys[0]]
    
    def add_node(self, new_node: str):
        """Add new node to cluster with minimal data movement"""
        self.nodes.append(new_node)
        self._build_ring()  # Rebuild ring
        print(f"➕ Added node: {new_node}")
    
    def remove_node(self, node: str):
        """Remove node from cluster"""
        if node in self.nodes:
            self.nodes.remove(node)
            self._build_ring()  # Rebuild ring
            print(f"➖ Removed node: {node}")

# Usage example
def example_sharding():
    shard = Shard(['db-a', 'db-b', 'db-c'])
    
    # Route keys to appropriate nodes
    test_keys = ['user-1000', 'user-2000', 'order-5000', 'product-3000']
    
    for key in test_keys:
        node = shard.get_node(key)
        print(f"🔗 Key '{key}' → Node '{node}'")
    
    # Demonstrate minimal movement when adding node
    print("\n--- Adding new node ---")
    shard.add_node('db-d')
    
    for key in test_keys:
        new_node = shard.get_node(key)
        print(f"🔗 Key '{key}' → Node '{new_node}'")

if __name__ == "__main__":
    example_sharding()