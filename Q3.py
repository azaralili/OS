import re
import graphviz
import subprocess
import platform

# Open the processes.txt file and read its contents
with open("processes3.txt", "r") as file:
    contents = file.read()

# Split the contents by each process and parent ID pair
pairs = re.findall("Process ID: (\d+)\nParent process ID: (\d+)", contents)

# Create a graph using the graphviz library
graph = graphviz.Digraph()

# Create a dictionary to keep track of nodes and their levels
node_levels = {}

# Add each process and its parent as a node in the graph
for child_id, parent_id in pairs:
    # Add the child node with its process ID and level
    if child_id not in node_levels:
        node_levels[child_id] = 1
        graph.node(child_id, label="Process ID: {}\nLevel: {}".format(child_id, node_levels[child_id]))
    # Add the parent node with its process ID and level
    if parent_id not in node_levels:
        node_levels[parent_id] = node_levels[child_id] + 1
        graph.node(parent_id, label="Process ID: {}\nLevel: {}".format(parent_id, node_levels[parent_id]))
    # Add an edge from the parent to the child
    graph.edge(parent_id, child_id)

# Render the graph to a PDF file
graph.render("process_tree")

# Open the PDF file using the default PDF viewer on the system
if platform.system() == "Windows":
    subprocess.run(['cmd', '/c', 'start', '', 'process_tree.pdf'], check=True)
else:
    subprocess.run(['xdg-open', 'process_tree.pdf'], check=True)
