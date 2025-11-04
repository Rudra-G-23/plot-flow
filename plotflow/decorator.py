"""
The @Pipeline Decorator

This module defines the core decorator used to register pipeline steps.
"""

from typing import Optional, List, Dict, Any, Callable
from .registry import register_node

class Pipeline:
    """
    A decorator to register a function as a node in a visual pipeline.

    Attributes:
        rank (int): A unique integer ID for this node.
        name (Optional[str]): A display name. If None, the function's
                              name is used.
        connect (Optional[List[int]]): A list of rank IDs that this
                                       node takes as input.
        meta (Optional[Dict[str, Any]]): Extra metadata for plotting or logic.
    """
    def __init__(
        self,
        rank: int,
        name: Optional[str] = None,
        connect: Optional[List[int]] = None,
        meta: Optional[Dict[str, Any]] = None
    ):
        if not isinstance(rank, int):
            raise TypeError("The 'rank' argument must be an integer.")
            
        self.rank = rank
        self.name = name
        self.connect = connect or []
        self.meta = meta or {}

    def __call__(self, func: Callable) -> Callable:
        """
        Called when the decorator is applied to a function.
        Registers the function and its metadata.
        """
        register_node(
            func=func,
            rank=self.rank,
            name=self.name,
            connect=self.connect,
            meta=self.meta
        )
        # Return the original function so it remains callable
        return func