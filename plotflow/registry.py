"""
Node Registry

This module provides a global registry to store and retrieve
pipeline nodes defined by the @Pipeline decorator.
"""

from typing import Dict, Any, List, Optional

# The _REGISTRY stores all node definitions, keyed by their unique rank.
_REGISTRY: Dict[int, Dict[str, Any]] = {}

class DuplicateRankError(Exception):
    """Raised when a rank is registered more than once."""
    pass

def register_node(
    func: callable,
    rank: int,
    name: Optional[str],
    connect: Optional[List[int]],
    meta: Optional[Dict[str, Any]]
) -> None:
    """
    Adds a node definition to the global registry.

    Args:
        func: The decorated function.
        rank: The unique integer ID for the node.
        name: The display name for the node. Defaults to function name
              or rank if no name or function name is available.
        connect: List of ranks this node depends on (inputs).
        meta: Optional dictionary of metadata.

    Raises:
        DuplicateRankError: If the rank is already registered.
    """
    if rank in _REGISTRY:
        raise DuplicateRankError(
            f"Error: Rank {rank} is already registered. "
            f"Node '{_REGISTRY[rank]['name']}' is already using this rank."
        )
    
    # Determine the node name
    node_name = name or func.__name__.replace("_", " ").title() or str(rank)

    _REGISTRY[rank] = {
        "name": node_name,
        "rank": rank,
        "connect": connect or [],
        "meta": meta or {},
        "func": func
    }

def get_registry() -> Dict[int, Dict[str, Any]]:
    """Returns a copy of the current node registry."""
    return _REGISTRY.copy()

def clear_registry() -> None:
    """
    Clears all nodes from the registry.
    
    This is essential for use in interactive environments like
    Jupyter notebooks to allow re-defining pipelines.
    """
    _REGISTRY.clear()