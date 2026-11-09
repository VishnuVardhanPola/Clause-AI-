from typing import TypedDict, List
from utils.llm_factory import get_llm
from langchain_core.messages import HumanMessage


# -------------------------------------------------
# SHARED STATE
# -------------------------------------------------
class ContractState(TypedDict):
    contract_text: str
    contract_id: str
    shared_memory: List[str]
    retrieved_clauses: List[str]
    compliance: List[dict]
    finance: List[dict]
    legal: List[dict]
    operations: List[dict]
    final_report: str


llm = get_llm()

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def find_sentence(text: str, keyword: str):
    for sentence in text.split("."):
        if keyword.lower() in sentence.lower():
            return sentence.strip()
    return ""


def generate_summary(clause_type: str, clause_text: str):
    """
    Uses LLM to generate natural explanation of clause
    """

    prompt = f"""
You are a legal assistant.

Explain the following clause in simple and clear language.

Clause Type: {clause_type}
Clause Text: "{clause_text}"

Include:
- What the clause means
- How it appears in this contract
- What risks it introduces
- How those risks can be reduced

Write in 5–6 short sentences using plain English.
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response


def build_clause(
    clause_type,
    category,
    explanation,
    why_it_matters,
    risk,
    counter_measure,
    source_sentence,
    contract_id,
    severity,
    confidence
):
    summary = generate_summary(clause_type, source_sentence)

    return {
        "clause_type": clause_type,
        "category": category,
        "explanation": explanation,
        "how_it_appears": f"\"{source_sentence}.\"",
        "why_it_matters": why_it_matters,
        "risk_or_note": risk,
        "countermeasures": counter_measure,
        "summary": summary,
        "severity": severity,
        "confidence": f"{confidence}%",
        "source_document": contract_id
    }


# -------------------------------------------------
# COMPLIANCE AGENT
# -------------------------------------------------
def compliance_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    findings = []

    sentence = find_sentence(text, "confidential")

    if sentence:
        findings.append(build_clause(
            "Confidentiality Clause",
            "Compliance",
            "Requires parties to protect sensitive information.",
            "Prevents misuse of confidential data.",
            "Vague scope may over-restrict or under-protect.",
            "Clearly define confidential data and exclusions.",
            sentence,
            doc,
            "Medium",
            90
        ))

        memory.append("Compliance agent reviewed confidentiality clause.")

    return {
        "compliance": findings,
        "shared_memory": memory
    }


# -------------------------------------------------
# FINANCE AGENT
# -------------------------------------------------
def finance_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    findings = []

    sentence = find_sentence(text, "payment")

    if sentence:
        findings.append(build_clause(
            "Payment Terms Clause",
            "Finance",
            "Specifies when and how payments must be made.",
            "Ensures predictable revenue flow.",
            "Delays or disputes over payments.",
            "Add clear deadlines, amounts, and penalties.",
            sentence,
            doc,
            "High",
            92
        ))

        memory.append("Finance agent reviewed payment terms.")

    return {
        "finance": findings,
        "shared_memory": memory
    }


# -------------------------------------------------
# LEGAL AGENT
# -------------------------------------------------
def legal_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    findings = []

    sentence = find_sentence(text, "termination")

    if sentence:
        findings.append(build_clause(
            "Termination Clause",
            "Legal",
            "Describes how the contract can be ended.",
            "Protects parties from sudden termination.",
            "One-sided termination rights.",
            "Include notice period and mutual rights.",
            sentence,
            doc,
            "High",
            94
        ))

        memory.append("Legal agent reviewed termination clause.")

    return {
        "legal": findings,
        "shared_memory": memory
    }


# -------------------------------------------------
# OPERATIONS AGENT
# -------------------------------------------------
def operations_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    findings = []

    sentence = find_sentence(text, "service level")

    if sentence:
        findings.append(build_clause(
            "Service Level Agreement (SLA)",
            "Operations",
            "Defines service quality and uptime standards.",
            "Ensures operational reliability.",
            "Weak enforcement if no penalties.",
            "Add KPIs, penalties, and escalation process.",
            sentence,
            doc,
            "Medium",
            88
        ))

        memory.append("Operations agent reviewed SLA clause.")

    return {
        "operations": findings,
        "shared_memory": memory
    }
