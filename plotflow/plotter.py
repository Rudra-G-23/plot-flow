"""
Pipeline Plotter

This module uses NetworkX and Matplotlib to visualize the pipeline graph.
It uses Graphviz (via pydot) for hierarchical layouts.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import Optional, Literal, Tuple

from .graph import build_graph

# Try to import graphviz_layout. Fail gracefully if pydot/graphviz isn't installed.
try:
    from networkx.drawing.nx_pydot import graphviz_layout
except ImportError:
    print(
        "Warning: `pydot` or `graphviz` not found. "
        "Falling back to `spring_layout`. "
        "Install `pydot` and Graphviz for hierarchical layouts."
    )
    graphviz_layout = None

def plot_flow(
    save_as: Optional[str] = None,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    show: bool = True,
    figsize: Tuple[int, int] = (10, 8),
    node_color: str = "#cceeff",
    node_size: int = 3000,
    font_size: int = 10,
) -> None:
    """
    Renders and displays or saves the defined pipeline graph.

    Args:
        save_as (Optional[str]): File path to save the plot (e.g., "pipeline.png").
                                 If None, plot is only shown.
        orientation (Literal): "vertical" (top-to-bottom) or
                               "horizontal" (left-to-right).
        show (bool): If True, display the plot using plt.show().
        figsize (Tuple[int, int]): The size of the matplotlib figure.
        node_color (str): The color of the nodes.
        node_size (int): The size of the nodes.
        font_size (int): The font size for node labels.
    """
    try:
        G = build_graph()
    except Exception as e:
        print(f"Error building graph: {e}")
        return

    plt.figure(figsize=figsize)
    
    # Get labels from node attributes
    labels = nx.get_node_attributes(G, 'label')

    # Determine layout
    if graphviz_layout:
        prog = "dot"
        
        # --- FIX IS HERE ---
        # 1. Set the layout direction on the graph object itself
        G.graph['rankdir'] = 'TB' if orientation == "vertical" else 'LR'
        
        # 2. Call graphviz_layout without the 'args' parameter
        pos = graphviz_layout(G, prog=prog)
        # -----------------

    else:
        # Fallback layout if pydot/graphviz is not available
        pos = nx.spring_layout(G, seed=42)

    # Draw the graph
    nx.draw(
        G,
        pos,
        labels=labels,
        with_labels=True,
        node_size=node_size,
        node_color=node_color,
        font_size=font_size,
        font_weight="bold",
        arrows=True,
        arrowstyle="-|>",
        arrowsize=20,
        node_shape="s",  # Use square shape as in the example
        edge_color="gray",
    )

    plt.title("Pipeline Flow", fontsize=16)
    
    if save_as:
        plt.savefig(save_as, bbox_inches="tight")
        print(f"Pipeline flow saved to '{save_as}'")

    if show:
        plt.show()
    else:
        plt.close() # Close plot to free memory if not showing