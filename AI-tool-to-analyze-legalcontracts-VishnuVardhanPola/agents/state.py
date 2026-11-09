from typing import TypedDict, List

class ContractState(TypedDict):
    contract_text: str
    clauses: List[str]
    risks: List[str]
    finance_points: List[str]
    final_summary: str
