import os
import sys

# --- This part is important for local testing ---
# Add the project's root directory (plotflow_project) to the Python path
# This allows the script to find the 'plotflow' package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ------------------------------------------------

from plotflow import Pipeline, plot_flow, clear_registry

def test_generate_plot():
    """
    Defines the 10-node graph from your example
    and saves it to a file.
    """
    print("Running test: Generating test plot...")
    
    # Clear registry to ensure a clean state
    clear_registry()

    # --- Define all 10 nodes ---
    @Pipeline(rank=1, name="Start Data Ingest")
    def node_1(): pass

    @Pipeline(rank=5, name="Load External Rules")
    def node_5(): pass

    @Pipeline(rank=7, name="Load Validation Schema")
    def node_7(): pass

    @Pipeline(rank=2, connect=[1], name="Clean Data")
    def node_2(): pass

    @Pipeline(rank=3, connect=[1], name="Transform Data")
    def node_3(): pass

    @Pipeline(rank=4, connect=[1], name="Feature Engineer")
    def node_4(): pass

    @Pipeline(rank=6, connect=[2, 5], name="Apply Business Rules")
    def node_6(): pass

    @Pipeline(rank=8, connect=[3, 4, 7], name="Validate Features")
    def node_8(): pass

    @Pipeline(rank=9, connect=[6, 8], name="Aggregate Results")
    def node_9(): pass

    @Pipeline(rank=10, connect=[9], name="Generate Report")
    def node_10(): pass

    # Define the output file path (it will be saved in the root folder)
    output_filename = os.path.join(project_root, "test_pipeline.png")
    
    # Clean up old file if it exists
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # Plot the graph, but do not show it (show=False)
    # This is better for an automated test.
    plot_flow(
        save_as=output_filename,
        show=False, 
        orientation="vertical",
        figsize=(12, 10),
        font_size=9,
        node_color="#d1f0ff"
    )

    # Check that the file was created
    assert os.path.exists(output_filename)
    print(f"Success! Test plot successfully generated at: {output_filename}")

if __name__ == "__main__":
    test_generate_plot()