"""
This type stub file was generated by pyright.
"""

from redis.typing import EncodedT

REDIS_CLUSTER_HASH_SLOTS = ...
__all__ = ["key_slot", "REDIS_CLUSTER_HASH_SLOTS"]
def key_slot(key: EncodedT, bucket: int = ...) -> int:
    """Calculate key slot for a given key.
    See Keys distribution model in https://redis.io/topics/cluster-spec
    :param key - bytes
    :param bucket - int
    """
    ...

