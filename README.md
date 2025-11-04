# PlotFlow 
![img](assets/plot-flow-logo.png)

A minimal Python package for defining and visualizing simple pipeline graphs using decorators.

## 🚀 Installation

Ensure you have [Graphviz](https://graphviz.org/download/) installed on your system. This is required for the hierarchical layouts.

Then, install the package and its Python dependencies:

```bash
pip install networkx matplotlib pydot
# (If installing this as a local package)
pip install .
```

## ✨ How to Use

Define your pipeline steps using the `@Pipeline` decorator, then call `plot_flow()` to see the result.

1.  **Import:** `from plotflow import Pipeline, plot_flow, clear_registry`
2.  **Define Nodes:** Use `@Pipeline(rank, connect)` to define each step.
    * `rank`: A unique integer ID for the node.
    * `connect`: A list of `rank` IDs that this node receives input *from*.
3.  **Plot:** Call `plot_flow()` to render the graph.

> **Note:** If you are in a Jupyter Notebook and want to re-run a cell, call `clear_registry()` at the start to clear old definitions.

## ✍️ Example

This code defines a 10-step pipeline based on a complex flow diagram.

```python
import matplotlib.pyplot as plt
from plotflow import Pipeline, plot_flow, clear_registry

# Clear previous definitions (useful for notebooks)
clear_registry()

@Pipeline(rank=1, name="Start Data Ingest")
def start_ingest():
    pass

@Pipeline(rank=5, name="Load External Rules")
def load_rules():
    pass

@Pipeline(rank=7, name="Load Validation Schema")
def load_schema():
    pass

@Pipeline(rank=2, connect=[1], name="Clean Data")
def clean_data():
    pass

@Pipeline(rank=3, connect=[1], name="Transform Data")
def transform_data():
    pass

@Pipeline(rank=4, connect=[1], name="Feature Engineer")
def feature_engineer():
    pass

@Pipeline(rank=6, connect=[2, 5], name="Apply Business Rules")
def apply_rules():
    pass

@Pipeline(rank=8, connect=[3, 4, 7], name="Validate Features")
def validate_features():
    pass

@Pipeline(rank=9, connect=[6, 8], name="Aggregate Results")
def aggregate_results():
    pass

@Pipeline(rank=10, connect=[9], name="Generate Report")
def generate_report():
    pass

# --- Plot the graph ---
# This will generate and save 'my_pipeline.png' and show it.
plot_flow(
    save_as="my_pipeline.png",
    show=True,
    orientation="vertical",
    figsize=(12, 10),
    font_size=9,
    node_color="#d1f0ff"
)
```
## 📊 Output
![img](assets/test_pipeline.png)