"""
PlotFlow: Visualize Python Pipelines Easily.

This package provides a simple decorator-based system to define
and visualize directed acyclic graphs (DAGs) of your processing pipelines.

Available functions:
- Pipeline: Decorator to register a function as a pipeline node.
- plot_flow: Function to render and save the pipeline graph.
- clear_registry: Utility to clear all registered nodes (useful for notebooks).
"""

from .decorator import Pipeline
from .registry import clear_registry
from .plotter import plot_flow

__all__ = ["Pipeline", "plot_flow", "clear_registry"]