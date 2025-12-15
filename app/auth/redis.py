# app/auth/redis.py
"""
Simple in-memory JWT blacklist used during testing.

This removes the dependency on aioredis, which is incompatible
with Python 3.12 because it imports the removed distutils module.
"""

from typing import Set

# Local in-memory blacklist storage
_blacklist: Set[str] = set()

async def add_to_blacklist(jti: str, exp: int):
    """
    Add a token JTI to the blacklist.
    `exp` is ignored but kept for signature compatibility.
    """
    _blacklist.add(jti)

async def is_blacklisted(jti: str) -> bool:
    """Check whether a token's JTI is in the blacklist."""
    return jti in _blacklist