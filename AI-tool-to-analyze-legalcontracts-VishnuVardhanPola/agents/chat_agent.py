from utils.llm_factory import get_llm
from utils.vector_store import query_similar_clauses

llm = get_llm()

def chat_with_contract(contract_text: str, question: str):
    """
    Conversational QA over contracts + stored memory
    """

    retrieved_chunks = query_similar_clauses(question, top_k=5)

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an expert legal assistant.

Use the following contract context and memory to answer.

-------------------
CONTRACT TEXT:
{contract_text[:3000]}

-------------------
RETRIEVED CONTEXT:
{context}

-------------------
USER QUESTION:
{question}

Rules:
- Answer only using the provided context.
- If information is missing, say you cannot find it.
- Give clear, simple, professional answers.
"""

    return llm.invoke(prompt)
