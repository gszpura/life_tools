"""
Flowchart Generator - Converts Python pseudocode to flowchart diagrams
Uses AST to parse Python code and Graphviz to render flowcharts
"""

import ast
import argparse
import os
from typing import List, Tuple
from graphviz import Digraph


class FlowchartNode:
    """Represents a node in the flowchart"""
    def __init__(self, node_id: int, label: str, node_type: str = "box"):
        self.node_id = node_id
        self.label = label
        self.node_type = node_type

    def __repr__(self):
        return f"Node({self.node_id}, '{self.label}')"


class FlowchartGenerator(ast.NodeVisitor):
    """AST visitor that builds a flowchart from Python code"""

    def __init__(self):
        self.nodes: List[FlowchartNode] = []
        self.edges: List[Tuple[int, int, str]] = []
        self.node_counter = 0
        self.current_node_id = None

    def add_node(self, label: str, node_type: str = "box") -> int:
        """Add a node to the flowchart and return its ID"""
        node = FlowchartNode(self.node_counter, label, node_type)
        self.nodes.append(node)
        node_id = self.node_counter
        self.node_counter += 1
        return node_id

    def add_edge(self, from_id: int, to_id: int, label: str = ""):
        """Add an edge between two nodes"""
        self.edges.append((from_id, to_id, label))

    def visit_Assign(self, node: ast.Assign):
        """Handle assignment statements (function calls on RHS)"""
        # Check if the RHS is a function call
        if isinstance(node.value, ast.Call):
            func_name = self.get_function_name(node.value)
            var_name = self.get_variable_name(node.targets[0])
            label = f"{var_name} = {func_name}()"

            new_node_id = self.add_node(label)

            # Connect to previous node if exists
            if self.current_node_id is not None:
                self.add_edge(self.current_node_id, new_node_id)

            self.current_node_id = new_node_id

        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        """Handle while loops"""
        # Get the condition as a string
        condition = ast.unparse(node.test) if hasattr(ast, 'unparse') else "condition"

        # Create a node for the loop condition
        loop_start_id = self.add_node(f"while {condition}", "box")

        # Connect previous node to loop start
        if self.current_node_id is not None:
            self.add_edge(self.current_node_id, loop_start_id)

        # Save the loop start for back edge
        loop_entry = self.current_node_id
        self.current_node_id = loop_start_id

        # Process loop body
        loop_body_entry = self.current_node_id
        for stmt in node.body:
            self.visit(stmt)

        # Add back edge from last node in body to loop start
        if self.current_node_id is not None:
            self.add_edge(self.current_node_id, loop_start_id, "loop back")

        # The loop continues to whatever comes next
        # Keep current_node_id as loop_start_id for the next statement
        self.current_node_id = loop_start_id

    def visit_For(self, node: ast.For):
        """Handle for loops"""
        # Get the loop variable and iterable
        target = ast.unparse(node.target) if hasattr(ast, 'unparse') else "item"
        iter_expr = ast.unparse(node.iter) if hasattr(ast, 'unparse') else "iterable"

        # Create a node for the loop
        loop_start_id = self.add_node(f"for {target} in {iter_expr}", "box")

        # Connect previous node to loop start
        if self.current_node_id is not None:
            self.add_edge(self.current_node_id, loop_start_id)

        self.current_node_id = loop_start_id

        # Process loop body
        for stmt in node.body:
            self.visit(stmt)

        # Add back edge from last node in body to loop start
        if self.current_node_id is not None:
            self.add_edge(self.current_node_id, loop_start_id, "loop back")

        # The loop continues to whatever comes next
        self.current_node_id = loop_start_id

    def visit_If(self, node: ast.If):
        """Handle if/elif/else statements"""
        # Get the condition as a string
        condition = ast.unparse(node.test) if hasattr(ast, 'unparse') else "condition"

        # Create a node for the if condition
        if_node_id = self.add_node(f"if {condition}", "box")

        # Connect previous node to if statement
        if self.current_node_id is not None:
            self.add_edge(self.current_node_id, if_node_id)

        # Save the if node as the branch point
        branch_point = if_node_id

        # Process the 'if' body (true branch)
        self.current_node_id = if_node_id
        last_if_node = None
        for stmt in node.body:
            self.visit(stmt)
        last_if_node = self.current_node_id

        # Process the 'else' body (false branch) if it exists
        last_else_node = None
        if node.orelse:
            self.current_node_id = branch_point
            for stmt in node.orelse:
                self.visit(stmt)
            last_else_node = self.current_node_id

        # After if/else, we need to continue from the last executed branch
        # For simplicity, continue from the last if node
        # In a more complex implementation, we'd merge branches
        if last_else_node:
            self.current_node_id = last_else_node
        else:
            self.current_node_id = last_if_node

    def visit_Expr(self, node: ast.Expr):
        """Handle expression statements (standalone function calls)"""
        if isinstance(node.value, ast.Call):
            func_name = self.get_function_name(node.value)
            label = f"{func_name}()"

            new_node_id = self.add_node(label)

            if self.current_node_id is not None:
                self.add_edge(self.current_node_id, new_node_id)

            self.current_node_id = new_node_id

    def get_function_name(self, call_node: ast.Call) -> str:
        """Extract function name from a Call node"""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return "function"

    def get_variable_name(self, target_node) -> str:
        """Extract variable name from assignment target"""
        if isinstance(target_node, ast.Name):
            return target_node.id
        return "var"

    def generate_flowchart(self, code: str, output_file: str = "flowchart"):
        """Parse code and generate flowchart diagram"""
        # Parse the Python code
        tree = ast.parse(code)

        # Visit all nodes
        self.visit(tree)

        # Create Graphviz diagram
        dot = Digraph(comment='Flowchart', format='png')
        dot.attr(rankdir='TB')  # Top to bottom layout
        dot.attr('node', shape='box', style='rounded', fontname='Arial')

        # Add all nodes
        for node in self.nodes:
            dot.node(str(node.node_id), node.label)

        # Add all edges
        for from_id, to_id, label in self.edges:
            if label:
                dot.edge(str(from_id), str(to_id), label=label, color='blue')
            else:
                dot.edge(str(from_id), str(to_id))

        # Render the diagram
        dot.render(output_file, cleanup=True)
        print(f"Flowchart generated: {output_file}.png")

        return dot


def generate_flowchart_from_file(python_file: str, output_file: str = "flowchart"):
    """Generate a flowchart from a Python file"""
    with open(python_file, 'r') as f:
        code = f.read()

    generator = FlowchartGenerator()
    generator.generate_flowchart(code, output_file)

    return generator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate flowcharts from Python pseudocode files"
    )
    parser.add_argument(
        "input_file",
        help="Path to the Python pseudocode file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file name (without extension, default: same as input file name)",
        default=None
    )
    parser.add_argument(
        "-d", "--output-dir",
        help="Output directory (default: current directory)",
        default="."
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Print detailed information about nodes and edges",
        action="store_true"
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found")
        exit(1)

    # Determine output file name
    if args.output:
        output_name = args.output
    else:
        # Use input file name without extension
        input_basename = os.path.basename(args.input_file)
        output_name = os.path.splitext(input_basename)[0] + "_flowchart"

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Full output path
    output_path = os.path.join(args.output_dir, output_name)

    # Generate flowchart
    print(f"Generating flowchart from {args.input_file}...")
    generator = generate_flowchart_from_file(args.input_file, output_path)

    if args.verbose:
        print(f"\nFound {len(generator.nodes)} nodes:")
        for node in generator.nodes:
            print(f"  {node}")

        print(f"\nFound {len(generator.edges)} edges:")
        for from_id, to_id, label in generator.edges:
            label_str = f" ({label})" if label else ""
            print(f"  {from_id} -> {to_id}{label_str}")
