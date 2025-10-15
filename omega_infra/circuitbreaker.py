"""
OMEGA.INFRA: CircuitBreaker - Adaptive Protection
Prevents cascading failures in microservices
"""

import time
import asyncio
from typing import Callable, Awaitable, Any
from functools import wraps
from enum import Enum


class CircuitState(Enum):
    CLOSED = "CLOSED"       # Normal operation
    OPEN = "OPEN"           # Fail fast
    HALF_OPEN = "HALF_OPEN" # Testing recovery


class CircuitOpenError(Exception):
    """Raised when the circuit is open and calls are blocked."""
    pass


class CircuitBreaker:
    def __init__(self, name: str, max_failures: int = 5, reset_timeout: int = 60):
        self.name = name
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self.next_check_time = 0

    def protect(self, func: Callable):
        """Decorator to wrap async functions with circuit breaker logic"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check circuit state
            if self.state == CircuitState.OPEN:
                if time.time() < self.next_check_time:
                    raise CircuitOpenError(f"Circuit {self.name} is OPEN")
                else:
                    self.state = CircuitState.HALF_OPEN

            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e

        return wrapper

    def _on_success(self):
        """Reset circuit on successful call"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0

    def _on_failure(self):
        """Handle failure and potentially trip circuit"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.max_failures:
            self.state = CircuitState.OPEN
            self.next_check_time = time.time() + self.reset_timeout
            print(f"🚨 CIRCUIT {self.name} TRIPPED! State: OPEN")


# ================================
# USAGE EXAMPLE
# ================================
circuit_breaker = CircuitBreaker("payment_gateway", max_failures=3)

@circuit_breaker.protect
async def call_payment_gateway(amount: float):
    """Simulated payment gateway call"""
    await asyncio.sleep(0.1)
    # Simulate occasional failures
    if amount > 1000:
        raise Exception("Payment gateway timeout")
    return {"status": "success", "amount": amount}


# Example runner
if __name__ == "__main__":
    async def test_circuit():
        for amt in [100, 1200, 150, 2000]:
            try:
                result = await call_payment_gateway(amt)
                print(f"Payment result: {result}")
            except Exception as e:
                print(f"Call failed: {e}")
            await asyncio.sleep(0.1)

    asyncio.run(test_circuit())
