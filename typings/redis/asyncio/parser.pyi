"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional, TYPE_CHECKING, Tuple
from redis.asyncio.cluster import ClusterNode

if TYPE_CHECKING:
    ...
class CommandsParser:
    """
    Parses Redis commands to get command keys.

    COMMAND output is used to determine key locations.
    Commands that do not have a predefined key location are flagged with 'movablekeys',
    and these commands' keys are determined by the command 'COMMAND GETKEYS'.

    NOTE: Due to a bug in redis<7.0, this does not work properly
    for EVAL or EVALSHA when the `numkeys` arg is 0.
     - issue: https://github.com/redis/redis/issues/9493
     - fix: https://github.com/redis/redis/pull/9733

    So, don't use this with EVAL or EVALSHA.
    """
    __slots__ = ...
    def __init__(self) -> None:
        ...
    
    async def initialize(self, node: Optional[ClusterNode] = ...) -> None:
        ...
    
    async def get_keys(self, *args: Any) -> Optional[Tuple[str, ...]]:
        ...
    


