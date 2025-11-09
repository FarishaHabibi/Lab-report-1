import streamlit as st
from typing import Dict, List, Set
import graphviz

# ---------- BFS and DFS core algorithms ----------
def bfs(graph: Dict[str, List[str]], start: str) -> List[str]:
    visited = []
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            neighbours = sorted(graph.get(node, []))
            for n in neighbours:
                if n not in visited and n not in queue:
                    queue.append(n)
    return visited

def dfs(graph: Dict[str, List[str]], start: str, visited: Set[str] = None) -> List[str]:
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for n in sorted(graph.get(start, [])):
        if n not in visited:
            order.extend(dfs(graph, n, visited))
    return order

# ---------- Streamlit UI ----------
st.set_page_config(page_title="BFS & DFS Traversal", page_icon="🔍", layout="wide")
st.title("🔍 Graph Traversal Visualizer (BFS & DFS)")
st.caption("Explore Breadth-First and Depth-First Search on a directed graph.")

with st.sidebar:
    st.header("Graph Input")
    mode = st.radio("Select Graph Type", ["Sample", "Custom"], index=0)
    sample_edges = {
        'A': ['B', 'D'],
        'B': ['C', 'E', 'G'],
        'C': ['A'],
        'D': ['C'],
        'E': ['H'],
        'F': [],
        'G': ['F', 'H'],
        'H': []
    }

    if mode == "Sample":
        graph = sample_edges
        st.markdown("**Sample Graph Used:**\n\nA→B, A→D, B→C, B→E, B→G, C→A, D→C, E→H, G→F, G→H")
    else:
        edge_text = st.text_area(
            "Enter edges (one per line: source,target)",
            value="A,B\nA,D\nB,C\nB,E\nB,G\nC,A\nD,C\nE,H\nG,F\nG,H",
            height=160,
        )
        graph = {}
        for line in edge_text.splitlines():
            line = line.strip()
            if not line or ',' not in line:
                continue
            u, v = [x.strip() for x in line.split(',')]
            graph.setdefault(u, []).append(v)
            if v not in graph:
                graph.setdefault(v, [])

    start_node = st.selectbox("Start Node", sorted(graph.keys()), index=0)
    algo = st.radio("Select Algorithm", ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"])
    run_btn = st.button("Run Traversal", type="primary")

st.divider()

if run_btn:
    if algo.startswith("Breadth"):
        order = bfs(graph, start_node)
        st.success(f"BFS Traversal Order: {' → '.join(order)}")
    else:
        order = dfs(graph, start_node)
        st.success(f"DFS Traversal Order: {' → '.join(order)}")

    # Graph visualization
    g = graphviz.Digraph(format="png")
    g.attr(rankdir="LR")

    edges_in_order = set()
    for i in range(len(order) - 1):
        edges_in_order.add((order[i], order[i + 1]))

    for u, nbrs in graph.items():
        for v in nbrs:
            color = "#d32f2f" if (u, v) in edges_in_order else "#4285f4"
            penwidth = "3" if (u, v) in edges_in_order else "1"
            g.edge(u, v, color=color, penwidth=penwidth)

    st.graphviz_chart(g, use_container_width=True)

    st.subheader("Traversal Steps")
    for i, node in enumerate(order, start=1):
        st.write(f"{i}. Visited: {node}")
else:
    st.info("Select options and click **Run Traversal** to visualize BFS or DFS.")


import graphviz
print(graphviz.__version__)

