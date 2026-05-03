import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ui.components import (
    show_agent_timeline,
    show_event_stream,
    show_knowledge_graph
)

from app.config import Config
from memory.memory_manager import MemoryManager
from memory.graph_builder import GraphBuilder

memory = MemoryManager()


def run_app(workflow, bob, event_bus):
    st.set_page_config(layout="wide")

    st.markdown("""
    <h1 style='text-align: center;'>🧠 Aegis AI</h1>
    <h4 style='text-align: center;'>Autonomous Decision Intelligence System</h4>
    """, unsafe_allow_html=True)

    # ✅ STATE INIT
    if "result" not in st.session_state:
        st.session_state.result = None
    if "result_sim" not in st.session_state:
        st.session_state.result_sim = None

    # 🔹 INPUT
    query = st.text_input("Ask a business question")

    # 🔹 GLOBAL TOGGLE (FIXED)
    autonomous = st.toggle("⚙️ Autonomous Mode", value=Config.AUTONOMOUS_MODE)
    Config.AUTONOMOUS_MODE = autonomous

    # 🔹 RUN BUTTON
    if st.button("Run Analysis"):

        if not query.strip():
            st.warning("Please enter a valid query")
            return

        with st.spinner("Running AEDIS pipeline..."):
            result = workflow.run(query)
            st.session_state.result = result

    result = st.session_state.result

    if not result:
        return

    # =============================
    # 🔥 AUTONOMOUS ACTIONS
    # =============================
    if result.get("selected_actions"):
        st.subheader("🤖 Autonomous Actions")

        for a in result["selected_actions"]:
            st.write(f"• {a['name']} ({a['type']})")

    if result.get("execution_results"):
        st.subheader("⚡ Execution Results")

        for r in result["execution_results"]:
            st.json(r)

    # =============================
    # 📊 MAIN LAYOUT
    # =============================
    col1, col2, col3, col4, col5 = st.columns(5)

    # 🔹 INSIGHTS
    with col1:
        st.subheader("📊 Insights")
        st.write(result.get("analysis", "No insights"))

    # 🔹 REVENUE TREND
    with col2:
        st.subheader("📈 Revenue Trend")

        ml = result.get("ml_result", {})
        monthly = ml.get("monthly")

        if monthly is not None and not monthly.empty:
            st.line_chart(monthly.set_index("date")["revenue"])
        else:
            st.warning("No trend data available")

    # 🔹 MEMORY
    with col3:
        st.subheader("🧠 Learning from Past Decisions")

        history = memory.get_all()

        if not history:
            st.write("No past decisions yet")
        else:
            for m in history[-3:]:
                st.write(f"Query: {m.get('query')}")
                st.write(f"Outcome: {m.get('results')}")

    # 🔹 ADVANCED CHARTS
    with col4:
        st.subheader("📊 Advanced Analysis")

        data = result.get("data")

        if data:
            df = pd.DataFrame(data, columns=[
                "date", "region", "product", "revenue", "cost", "profit", "customer_id"
            ])

            st.line_chart(df["revenue"])

            # Safe plot
            try:
                plt.figure()
                plt.plot(df["revenue"])
                st.pyplot(plt)
            except Exception as e:
                st.write("Plot error:", e)

        else:
            st.write("No data available")

    # 🔹 WHAT-IF
    with col5:
        st.subheader("🔮 What-If Simulation")

        what_if_input = st.text_input("Scenario")

        if st.button("Run What-If"):
            from memory.what_if_engine import WhatIfEngine

            engine = WhatIfEngine()
            result_sim = engine.simulate(what_if_input, intensity=1.2)

            st.session_state.result_sim = result_sim

        if st.session_state.result_sim:
            st.json(st.session_state.result_sim)

    # =============================
    # 🎯 STRATEGY
    # =============================
    st.subheader("🎯 Strategy Recommendations")

    strategy = result.get("strategy", "No strategy generated")

    st.markdown(f"""
    <div style="background-color:#0e1117;padding:15px;border-radius:10px;">
    {strategy}
    </div>
    """, unsafe_allow_html=True)

    # =============================
    # 🔐 APPROVAL SYSTEM (FIXED FLOW)
    # =============================
    if result.get("selected_actions"):
        st.subheader("🛑 Approve Actions Before Execution")

        approved_actions = []

        for i, action in enumerate(result["selected_actions"]):
            approve = st.checkbox(
                f"{action['name']}",
                key=f"approve_{i}"
            )

            if approve:
                approved_actions.append(action)

        if st.button("🚀 Execute Approved Actions"):
            result["approved_actions"] = approved_actions

            new_result = workflow.run(result["query"])
            st.session_state.result = new_result
            st.success("Execution complete")

    # =============================
    # 🔮 PREDICTIONS
    # =============================
    if result.get("selected_actions"):
        st.subheader("🔮 Predicted Impact")

        for action in result["selected_actions"]:
            st.write(f"### {action['name']}")
            st.json(action.get("predicted_impact"))
            st.json(action.get("what_if"))

    # =============================
    # ⚡ EVENT STREAM (NEW 🔥)
    # =============================
    with st.expander("⚡ Event Stream"):
        events = event_bus.get_events()
        show_event_stream(events)

    # =============================
    # 🧠 KNOWLEDGE GRAPH
    # =============================
    kg = GraphBuilder().get_graph()

    with st.expander("🧠 Knowledge Graph Brain"):
        show_knowledge_graph(kg)

    # =============================
    # 📜 LOGS
    # =============================
    with st.expander("⚙️ IBM Bob Logs"):
        for log in bob.get_logs():
            st.text(log)

    # =============================
    # 🧠 MEMORY
    # =============================
    with st.expander("🧠 System Memory"):
        for h in memory.get_all()[-5:]:
            st.json(h)

    # =============================
    # 📊 METRICS
    # =============================
    st.metric("Confidence Score", result.get("confidence", 0))
    st.metric("Total Revenue", "$1.2M")
    st.metric("Profit Margin", "23%")