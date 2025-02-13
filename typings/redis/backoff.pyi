"""
This type stub file was generated by pyright.
"""

from abc import ABC, abstractmethod

DEFAULT_CAP = ...
DEFAULT_BASE = ...
class AbstractBackoff(ABC):
    """Backoff interface"""
    def reset(self): # -> None:
        """
        Reset internal state before an operation.
        `reset` is called once at the beginning of
        every call to `Retry.call_with_retry`
        """
        ...
    
    @abstractmethod
    def compute(self, failures): # -> None:
        """Compute backoff in seconds upon failure"""
        ...
    


class ConstantBackoff(AbstractBackoff):
    """Constant backoff upon failure"""
    def __init__(self, backoff) -> None:
        """`backoff`: backoff time in seconds"""
        ...
    
    def compute(self, failures): # -> Any:
        ...
    


class NoBackoff(ConstantBackoff):
    """No backoff upon failure"""
    def __init__(self) -> None:
        ...
    


class ExponentialBackoff(AbstractBackoff):
    """Exponential backoff upon failure"""
    def __init__(self, cap=..., base=...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """
        ...
    
    def compute(self, failures): # -> float:
        ...
    


class FullJitterBackoff(AbstractBackoff):
    """Full jitter backoff upon failure"""
    def __init__(self, cap=..., base=...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """
        ...
    
    def compute(self, failures): # -> float:
        ...
    


class EqualJitterBackoff(AbstractBackoff):
    """Equal jitter backoff upon failure"""
    def __init__(self, cap=..., base=...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """
        ...
    
    def compute(self, failures): # -> float:
        ...
    


class DecorrelatedJitterBackoff(AbstractBackoff):
    """Decorrelated jitter backoff upon failure"""
    def __init__(self, cap=..., base=...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """
        ...
    
    def reset(self): # -> None:
        ...
    
    def compute(self, failures): # -> float:
        ...
    


def default_backoff(): # -> EqualJitterBackoff:
    ...

