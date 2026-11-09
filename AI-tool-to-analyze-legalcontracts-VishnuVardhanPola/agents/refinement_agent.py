from agents.roles import ContractState
from utils.vector_store import store_agent_results


# -----------------------------------
# HELPER FUNCTIONS
# -----------------------------------

def deduplicate_clauses(clauses):
    seen = set()
    unique = []

    for c in clauses:
        key = (c["clause_type"], c.get("source_document", ""))
        if key not in seen:
            unique.append(c)
            seen.add(key)

    return unique


def severity_rank(sev):
    return {"High": 3, "Medium": 2, "Low": 1}.get(sev, 0)


def sort_by_risk(clauses):
    return sorted(
        clauses,
        key=lambda x: severity_rank(x.get("severity", "")),
        reverse=True
    )


def build_executive_summary(state: ContractState):
    summary = []

    if state["compliance"]:
        summary.append(f"{len(state['compliance'])} compliance-related clauses detected.")

    if state["finance"]:
        summary.append(f"{len(state['finance'])} financial risk clauses detected.")

    if state["legal"]:
        summary.append(f"{len(state['legal'])} legal clauses requiring attention.")

    if state["operations"]:
        summary.append(f"{len(state['operations'])} operational obligation clauses found.")

    return summary


# -----------------------------------
# REFINEMENT AGENT
# -----------------------------------

def refinement_agent(state: ContractState):

    contract_id = state.get("contract_id", "latest_contract")

    # Deduplicate
    compliance = deduplicate_clauses(state["compliance"])
    finance = deduplicate_clauses(state["finance"])
    legal = deduplicate_clauses(state["legal"])
    operations = deduplicate_clauses(state["operations"])

    # Sort by severity
    compliance = sort_by_risk(compliance)
    finance = sort_by_risk(finance)
    legal = sort_by_risk(legal)
    operations = sort_by_risk(operations)

    # Store results in Pinecone
    store_agent_results(contract_id, "compliance", compliance)
    store_agent_results(contract_id, "finance", finance)
    store_agent_results(contract_id, "legal", legal)
    store_agent_results(contract_id, "operations", operations)

    # Build memory summary
    memory = state.get("shared_memory", [])
    memory.append("Refinement Agent consolidated, ranked, and stored all agent outputs.")

    memory.extend(build_executive_summary({
        "compliance": compliance,
        "finance": finance,
        "legal": legal,
        "operations": operations
    }))

    # Final state
    return {
        "compliance": compliance,
        "finance": finance,
        "legal": legal,
        "operations": operations,
        "shared_memory": memory
    }
