import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def show_header():
    st.title("🧠 Aedis AI")

def show_logs(logs):
    for log in logs:
        st.text(log)

def show_agent_timeline(events):
    st.subheader("🧠 Agent Timeline")

    for e in events:
        st.markdown(f"""
        **{e.agent.upper()}** → {e.step}  
        `{e.message}`
        """)
def show_causal_chain(graph, node):
    st.subheader(f"🔗 Causal Chain for {node}")

    edges = graph.query(node)

    for src, dst, data in edges:
        st.write(f"{src} → {data['relation']} → {dst}")

def show_event_stream(events):
    st.subheader("⚡ Event Stream")

    for e in events[-10:]:
        st.text(f"[{e.agent}] {e.step}: {e.message}")

def show_knowledge_graph(graph):
    st.subheader("🧠 Knowledge Graph")

    G = graph.graph

    if len(G.nodes) == 0:
        st.write("No knowledge yet")
        return

    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    st.pyplot(plt)
