import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -------------------------------------------------
# CONFIG
# -------------------------------------------------
INDEX_NAME = "clauseai-index"
EMBEDDING_DIM = 384


# -------------------------------------------------
# PINECONE INIT
# -------------------------------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


def get_index():
    if INDEX_NAME not in pc.list_indexes().names():
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


index = get_index()


# -------------------------------------------------
# EMBEDDINGS
# -------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------------------------------------
# SPLITTER
# -------------------------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


# -------------------------------------------------
# STORE FULL CONTRACT
# -------------------------------------------------
def index_contract(contract_id: str, text: str):
    chunks = splitter.split_text(text)
    vectors = []

    for i, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk)

        vectors.append((
            f"{contract_id}-chunk-{i}",
            vector,
            {
                "text": chunk,
                "namespace": "contracts",
                "contract_id": contract_id
            }
        ))

    if vectors:
        index.upsert(vectors)

    return len(chunks)


# -------------------------------------------------
# STORE AGENT RESULTS
# -------------------------------------------------
def store_agent_results(contract_id: str, agent_name: str, findings: list):
    vectors = []

    for i, item in enumerate(findings):

        content = f"""
Clause: {item['clause_type']}
Explanation: {item['explanation']}
Risk: {item['risk_or_note']}
Countermeasure: {item.get('countermeasures', '')}
Severity: {item.get('severity', '')}
"""

        vector = embeddings.embed_query(content)

        vectors.append((
            f"{contract_id}-{agent_name}-{i}",
            vector,
            {
                "text": content,
                "namespace": "agent_results",
                "agent": agent_name,
                "contract_id": contract_id
            }
        ))

    if vectors:
        index.upsert(vectors)


# -------------------------------------------------
# STORE FINAL REPORT
# -------------------------------------------------
def store_report(contract_id: str, report_text: str):

    vector = embeddings.embed_query(report_text)

    index.upsert([
        (
            f"{contract_id}-final-report",
            vector,
            {
                "text": report_text,
                "namespace": "reports",
                "contract_id": contract_id
            }
        )
    ])


# -------------------------------------------------
# RETRIEVE SIMILAR CONTENT
# -------------------------------------------------
def query_similar(query_text: str, top_k: int = 5, namespace: str | None = None):

    vector = embeddings.embed_query(query_text)

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    matches = results.get("matches", [])

    if namespace:
        matches = [
            m for m in matches
            if m["metadata"].get("namespace") == namespace
        ]

    return [
        m["metadata"].get("text", "")
        for m in matches
    ]
# ---------------------------------
# QUERY SIMILAR CLAUSES (CHATBOT)
# ---------------------------------
def query_similar_clauses(query_text: str, top_k: int = 5):
    vector = embeddings.embed_query(query_text)

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    return [
        match["metadata"].get("text", "")
        for match in results["matches"]
    ]
