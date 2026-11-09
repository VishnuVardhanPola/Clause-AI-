from langgraph.graph import StateGraph, END

from agents.roles import (
    ContractState,
    compliance_agent,
    finance_agent,
    legal_agent,
    operations_agent,
)

from agents.retrieval_agent import retrieval_agent
from agents.refinement_agent import refinement_agent
from reports.report_generator import generate_report


# ----------------------------------------
# REPORT NODE
# ----------------------------------------
def report_agent(state: ContractState):
    report = generate_report(
        state,
        tone=state.get("tone", "professional"),
        focus=state.get("focus", "balanced")
    )

    state["final_report"] = report
    return state


# ----------------------------------------
# BUILD GRAPH
# ----------------------------------------
def build_contract_graph():

    graph = StateGraph(ContractState)

    # -------- Nodes --------
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("compliance", compliance_agent)
    graph.add_node("finance", finance_agent)
    graph.add_node("legal", legal_agent)
    graph.add_node("operations", operations_agent)
    graph.add_node("refinement", refinement_agent)
    graph.add_node("report", report_agent)

    # -------- Entry --------
    graph.set_entry_point("retrieval")

    # -------- Flow --------
    graph.add_edge("retrieval", "compliance")
    graph.add_edge("compliance", "finance")
    graph.add_edge("finance", "legal")
    graph.add_edge("legal", "operations")
    graph.add_edge("operations", "refinement")
    graph.add_edge("refinement", "report")
    graph.add_edge("report", END)

    return graph.compile()
