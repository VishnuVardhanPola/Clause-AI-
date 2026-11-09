from langgraph.graph import StateGraph

def build_workflow():
    workflow = StateGraph(dict)
    workflow.set_entry_point("plan")
    return workflow
