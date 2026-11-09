from typing import TypedDict, List
from utils.llm_factory import get_llm

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
    audit_log: List[str]


llm = get_llm()

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
RED_FLAG_KEYWORDS = [
    "indemnify",
    "unlimited liability",
    "penalty",
    "without notice",
    "sole discretion"
]

SEVERITY_SCORE = {
    "Low": 3,
    "Medium": 6,
    "High": 9
}


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def find_sentence(text: str, keyword: str):
    for sentence in text.split("."):
        if keyword.lower() in sentence.lower():
            return sentence.strip()
    return ""


def detect_red_flags(text: str):
    flags = []
    for word in RED_FLAG_KEYWORDS:
        if word in text.lower():
            flags.append(word)
    return flags


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
    # LLM generated natural explanation
    summary = llm.explain_clause(clause_type, source_sentence)

    # Risk score
    risk_score = SEVERITY_SCORE.get(severity, 5)

    # Red flags
    red_flags = detect_red_flags(source_sentence)

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
        "risk_score": risk_score,
        "red_flags": red_flags,
        "why_flagged": [
            f"Keyword match for {clause_type}",
            f"Severity level: {severity}",
            f"Detected red flags: {', '.join(red_flags) if red_flags else 'None'}"
        ],
        "source_document": contract_id
    }


# -------------------------------------------------
# COMPLIANCE AGENT
# -------------------------------------------------
def compliance_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    audit = state.get("audit_log", [])
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
        audit.append("Compliance agent executed.")

    return {
        "compliance": findings,
        "shared_memory": memory,
        "audit_log": audit
    }


# -------------------------------------------------
# FINANCE AGENT
# -------------------------------------------------
def finance_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    audit = state.get("audit_log", [])
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
        audit.append("Finance agent executed.")

    return {
        "finance": findings,
        "shared_memory": memory,
        "audit_log": audit
    }


# -------------------------------------------------
# LEGAL AGENT
# -------------------------------------------------
def legal_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    audit = state.get("audit_log", [])
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
        audit.append("Legal agent executed.")

    return {
        "legal": findings,
        "shared_memory": memory,
        "audit_log": audit
    }


# -------------------------------------------------
# OPERATIONS AGENT
# -------------------------------------------------
def operations_agent(state: ContractState):
    text = state["contract_text"]
    doc = state["contract_id"]

    memory = state.get("shared_memory", [])
    audit = state.get("audit_log", [])
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
        audit.append("Operations agent executed.")

    return {
        "operations": findings,
        "shared_memory": memory,
        "audit_log": audit
    }
