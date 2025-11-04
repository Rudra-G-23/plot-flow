"""
Graph Builder

This module converts the node registry into a NetworkX
Directed Acyclic Graph (DAG) and validates it.
"""

import networkx as nx
from typing import Dict, Any
from .registry import get_registry

class NodeConnectionError(Exception):
    """Raised when a node tries to connect to a non-existent rank."""
    pass

class CycleError(Exception):
    """Raised when a cycle is detected in the graph."""
    pass

def build_graph() -> nx.DiGraph:
    """
    Builds a NetworkX DiGraph from the registered nodes.

    Returns:
        nx.DiGraph: A directed graph with nodes and edges.

    Raises:
        NodeConnectionError: If a connection points to an invalid rank.
        CycleError: If the resulting graph contains one or more cycles.
    """
    registry = get_registry()
    if not registry:
        raise ValueError("No pipeline nodes have been registered. "
                         "Use the @Pipeline decorator to define nodes.")

    G = nx.DiGraph()
    node_labels = {}

    # Add all nodes first
    for rank, node_data in registry.items():
        G.add_node(rank)
        node_labels[rank] = node_data['name']
    
    # Set labels as a graph attribute for the plotter
    nx.set_node_attributes(G, node_labels, 'label')

    # Add all edges
    for rank, node_data in registry.items():
        for source_rank in node_data['connect']:
            # Check if the source node exists before connecting
            if source_rank not in registry:
                raise NodeConnectionError(
                    f"Node {rank} ('{node_data['name']}') tries to connect "
                    f"from non-existent rank {source_rank}."
                )
            # Add edge: from source -> to current node
            G.add_edge(source_rank, rank)

    # Validate that the graph is a DAG
    if not nx.is_directed_acyclic_graph(G):
        cycles = list(nx.simple_cycles(G))
        raise CycleError(f"A cycle was detected in the pipeline: {cycles}")

    return G