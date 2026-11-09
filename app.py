import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# -----------------------------
# ENV SETUP
# -----------------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# -----------------------------
# IMPORTS
# -----------------------------
from parser.document_parser import extract_text
from graph.contract_graph import build_contract_graph
from utils.vector_store import index_contract, store_report
from reports.report_generator import generate_report
from utils.pdf_utils import generate_pdf
from agents.chat_agent import chat_with_contract

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "final_state" not in st.session_state:
    st.session_state.final_state = None
if "report" not in st.session_state:
    st.session_state.report = None
if "all_text" not in st.session_state:
    st.session_state.all_text = None
if "chat_answer" not in st.session_state:
    st.session_state.chat_answer = None

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ClauseAI – Contract Intelligence",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div style="padding:2rem;border-radius:15px;
background:linear-gradient(135deg,#6366F1,#4F46E5);
color:white">
<h1>📄 ClauseAI</h1>
<p>AI-powered contract intelligence using LangGraph, Gemini & Pinecone</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Report Settings")

tone = st.sidebar.selectbox(
    "Report Tone",
    ["professional", "business-friendly", "simple", "strict-legal"]
)

focus = st.sidebar.selectbox(
    "Report Focus",
    ["balanced", "risk-heavy", "compliance-heavy", "financial-heavy"]
)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload Contracts",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# -----------------------------
# PROCESS FILES
# -----------------------------
def process_file(file):
    file_type = file.name.split(".")[-1]
    text = extract_text(file, file_type)
    index_contract(file.name, text)
    return f"\n\n--- {file.name} ---\n{text}"

# -----------------------------
# LOAD FILES
# -----------------------------
if uploaded_files:
    with st.spinner("📑 Extracting & indexing contracts..."):
        with ThreadPoolExecutor() as executor:
            texts = list(executor.map(process_file, uploaded_files))

    st.session_state.all_text = "".join(texts)
    st.success(f"{len(uploaded_files)} contracts processed")

    with st.expander("📜 View Extracted Text"):
        st.text_area("", st.session_state.all_text, height=300)

# -----------------------------
# RUN ANALYSIS
# -----------------------------
if st.button("🚀 Run AI Analysis") and st.session_state.all_text:
    with st.spinner("🤖 Running multi-agent analysis..."):
        graph = build_contract_graph()

        st.session_state.final_state = graph.invoke({
            "contract_text": st.session_state.all_text,
            "contract_id": "Multiple Documents",
            "shared_memory": [],
            "retrieved_clauses": [],
            "compliance": [],
            "finance": [],
            "legal": [],
            "operations": [],
            "final_report": ""
        })

    st.session_state.report = generate_report(
        st.session_state.final_state,
        tone,
        focus
    )

    store_report("Multiple Documents", st.session_state.report)
    st.success("✅ Analysis completed")

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
if st.session_state.final_state:

    tabs = st.tabs([
        "⚖️ Compliance",
        "💰 Finance",
        "📜 Legal",
        "⚙️ Operations",
        "📑 Final Report",
        "📥 Download PDF",
        "💬 Chat",
        "🧠 Memory"
    ])

    def render(findings):
        if not findings:
            st.info("No issues detected.")
            return
        for c in findings:
            with st.expander(c["clause_type"]):
                st.write("Category:", c["category"])
                st.write("Explanation:", c["explanation"])
                st.write("How it appears:", c["how_it_appears"])
                st.write("Why it matters:", c["why_it_matters"])
                st.write("Risk:", c["risk_or_note"])
                st.write("Countermeasure:", c.get("countermeasures", ""))
                st.write("Severity:", c.get("severity", ""))
                st.write("Confidence:", c.get("confidence", ""))
                st.write("Summary:", c.get("summary", ""))
                st.write("Source:", c.get("source_document", ""))

    with tabs[0]:
        render(st.session_state.final_state["compliance"])

    with tabs[1]:
        render(st.session_state.final_state["finance"])

    with tabs[2]:
        render(st.session_state.final_state["legal"])

    with tabs[3]:
        render(st.session_state.final_state["operations"])

    with tabs[4]:
        st.text_area("Generated Report", st.session_state.report, height=400)

    with tabs[5]:
        if st.button("Generate PDF"):
            pdf_path = generate_pdf(
                st.session_state.report,
                "ClauseAI_Report.pdf"
            )
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download Report",
                    f,
                    file_name="ClauseAI_Report.pdf"
                )

    with tabs[6]:
        question = st.text_input("Ask a question about your contracts")

        if st.button("Ask"):
            st.session_state.chat_answer = chat_with_contract(
                st.session_state.all_text,
                question
            )

        if st.session_state.chat_answer:
            st.write(st.session_state.chat_answer)

    with tabs[7]:
        st.write(st.session_state.final_state["shared_memory"])

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("ClauseAI © 2026 | LangGraph • Gemini • Pinecone • Streamlit")
