from graphviz import Digraph

# Define components and edges
def draw_flowchart(components,edges):
    # Create a Digraph object
    flowchart = Digraph('Flowchart', format='png')

    # Add nodes and edges based on components and edges
    for component_type, nodes in components.items():
        for node in nodes:
            if component_type == 'decisions':
                flowchart.node(node, shape='diamond')  # Decisions represented as diamonds
            elif component_type == 'processes':
                flowchart.node(node, shape='rectangle')  # Processes represented as rectangles
            elif component_type == 'loops':
                flowchart.node(node, shape='parallelogram')  # Loops represented as parallelograms
            elif component_type == 'start/end':
                flowchart.node(node, shape='ellipse')  # Start/End represented as ellipses

    # Add edges to the flowchart
    for edge in edges:
        flowchart.edge(*edge)

    # Render the flowchart to a PNG file
    flowchart.render('flowchart', format='png', cleanup=True)
    print("Flowchart generated successfully.")