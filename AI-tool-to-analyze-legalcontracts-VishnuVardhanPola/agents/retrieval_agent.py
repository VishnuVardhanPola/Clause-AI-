import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from agents.roles import ContractState


# -------------------------------------------------
# CONFIG
# -------------------------------------------------
INDEX_NAME = "clauseai-index"
EMBEDDING_DIM = 384
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# -------------------------------------------------
# PINECONE INIT
# -------------------------------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


def get_index():
    existing = pc.list_indexes().names()

    if INDEX_NAME not in existing:
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc.Index(INDEX_NAME)


# -------------------------------------------------
# EMBEDDINGS (LOAD ONCE)
# -------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL
)


# -------------------------------------------------
# RETRIEVAL AGENT (LANGGRAPH NODE)
# -------------------------------------------------
def retrieval_agent(state: ContractState):
    """
    Retrieves similar contract chunks from Pinecone
    and injects them into graph state.
    """

    index = get_index()

    query_text = state["contract_text"][:1500]

    if not query_text.strip():
        return {"retrieved_clauses": []}

    query_vector = embeddings.embed_query(query_text)

    results = index.query(
        vector=query_vector,
        top_k=8,
        include_metadata=True
    )

    matches = results.get("matches", [])

    retrieved = []
    seen = set()

    for match in matches:
        metadata = match.get("metadata", {})
        namespace = metadata.get("namespace")

        # Only retrieve CONTRACT chunks (not agent results or reports)
        if namespace != "contracts":
            continue

        text = metadata.get("text", "")
        source = metadata.get("contract_id", "unknown")

        key = f"{text[:50]}-{source}"

        if text and key not in seen:
            retrieved.append({
                "text": text,
                "source_document": source
            })
            seen.add(key)

    return {
        "retrieved_clauses": retrieved
    }
