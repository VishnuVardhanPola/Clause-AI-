import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ClauseAI – Contract Intelligence",
    layout="wide"
)

# -----------------------------
# ENVIRONMENT SETUP
# -----------------------------

# Load local environment variables
load_dotenv(Path(__file__).parent / ".env")

# Load Streamlit Cloud secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

    if "PINECONE_API_KEY" in st.secrets:
        os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]

except Exception:
    # Allows the application to run locally without Streamlit secrets
    pass


# -----------------------------
# PROJECT IMPORTS
# -----------------------------
from parser.document_parser import extract_text
from graph.contract_graph import build_contract_graph
from utils.vector_store import index_contract
from reports.report_generator import generate_report
from utils.pdf_utils import generate_pdf
from agents.chat_agent import chat_with_contract


# -----------------------------
# SESSION STATE INITIALIZATION
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
# HEADER
# -----------------------------
st.markdown("""
<div style="
    padding: 2rem;
    border-radius: 15px;
    background: linear-gradient(135deg, #6366F1, #4F46E5);
    color: white;
">
    <h1>📄 ClauseAI</h1>
    <p>
        AI-powered contract intelligence using LangGraph, Gemini & Pinecone
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
st.sidebar.header("⚙️ Report Settings")

tone = st.sidebar.selectbox(
    "Report Tone",
    [
        "professional",
        "business-friendly",
        "simple",
        "strict-legal"
    ]
)

focus = st.sidebar.selectbox(
    "Report Focus",
    [
        "balanced",
        "risk-heavy",
        "compliance-heavy",
        "financial-heavy"
    ]
)


# -----------------------------
# FILE UPLOAD
# -----------------------------
st.subheader("📂 Upload Contracts")

uploaded_files = st.file_uploader(
    "Upload your PDF or DOCX contracts",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


# -----------------------------
# PROCESS FILES
# -----------------------------
def process_file(file):

    file_type = file.name.split(".")[-1].lower()

    text = extract_text(file, file_type)

    if not text:
        return f"\n\n--- {file.name} ---\nNo text could be extracted."

    index_contract(file.name, text)

    return f"\n\n--- {file.name} ---\n{text}"


# -----------------------------
# LOAD AND EXTRACT FILES
# -----------------------------
if uploaded_files:

    if st.button("📥 Process Uploaded Contracts"):

        try:
            with st.spinner("📑 Extracting and indexing contracts..."):

                with ThreadPoolExecutor() as executor:
                    texts = list(
                        executor.map(process_file, uploaded_files)
                    )

                st.session_state.all_text = "".join(texts)

                # Reset previous analysis when new files are uploaded
                st.session_state.final_state = None
                st.session_state.report = None
                st.session_state.chat_answer = None

            st.success(
                f"Successfully processed {len(uploaded_files)} contract(s)."
            )

        except Exception as e:
            st.error(f"Error processing contracts: {str(e)}")


# -----------------------------
# DISPLAY EXTRACTED TEXT
# -----------------------------
if st.session_state.all_text:

    with st.expander("📜 View Extracted Contract Text"):

        st.text_area(
            "Extracted Text",
            st.session_state.all_text,
            height=300
        )


# -----------------------------
# RUN AI ANALYSIS
# -----------------------------
if st.session_state.all_text:

    if st.button("🚀 Run AI Analysis"):

        try:
            with st.spinner("🤖 Running multi-agent AI analysis..."):

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

            st.success("✅ Contract analysis completed successfully!")

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")


# -----------------------------
# DISPLAY ANALYSIS RESULTS
# -----------------------------
if st.session_state.final_state:

    st.divider()

    st.header("📊 Contract Analysis Results")

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


    # -----------------------------
    # FINDINGS RENDER FUNCTION
    # -----------------------------
    def render(findings):

        if not findings:
            st.info("No issues detected.")
            return

        for c in findings:

            with st.expander(c.get("clause_type", "Contract Finding")):

                st.write("**Category:**", c.get("category", ""))

                st.write(
                    "**Explanation:**",
                    c.get("explanation", "")
                )

                st.write(
                    "**How it appears:**",
                    c.get("how_it_appears", "")
                )

                st.write(
                    "**Why it matters:**",
                    c.get("why_it_matters", "")
                )

                st.write(
                    "**Risk:**",
                    c.get("risk_or_note", "")
                )

                st.write(
                    "**Countermeasure:**",
                    c.get("countermeasures", "")
                )

                st.write(
                    "**Severity:**",
                    c.get("severity", "")
                )

                st.write(
                    "**Confidence:**",
                    c.get("confidence", "")
                )

                st.write(
                    "**Summary:**",
                    c.get("summary", "")
                )

                st.write(
                    "**Source:**",
                    c.get("source_document", "")
                )


    # -----------------------------
    # COMPLIANCE
    # -----------------------------
    with tabs[0]:

        st.subheader("⚖️ Compliance Analysis")

        render(
            st.session_state.final_state.get("compliance", [])
        )


    # -----------------------------
    # FINANCE
    # -----------------------------
    with tabs[1]:

        st.subheader("💰 Financial Analysis")

        render(
            st.session_state.final_state.get("finance", [])
        )


    # -----------------------------
    # LEGAL
    # -----------------------------
    with tabs[2]:

        st.subheader("📜 Legal Analysis")

        render(
            st.session_state.final_state.get("legal", [])
        )


    # -----------------------------
    # OPERATIONS
    # -----------------------------
    with tabs[3]:

        st.subheader("⚙️ Operational Analysis")

        render(
            st.session_state.final_state.get("operations", [])
        )


    # -----------------------------
    # FINAL REPORT
    # -----------------------------
    with tabs[4]:

        st.subheader("📑 Generated Contract Report")

        st.text_area(
            "Final Report",
            st.session_state.report or "",
            height=450
        )


    # -----------------------------
    # DOWNLOAD PDF
    # -----------------------------
    with tabs[5]:

        st.subheader("📥 Download Analysis Report")

        if st.button("Generate PDF"):

            try:

                pdf_path = generate_pdf(
                    st.session_state.report,
                    "ClauseAI_Report.pdf"
                )

                with open(pdf_path, "rb") as pdf_file:

                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_file,
                        file_name="ClauseAI_Report.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:

                st.error(f"PDF generation failed: {str(e)}")


    # -----------------------------
    # CHAT WITH CONTRACT
    # -----------------------------
    with tabs[6]:

        st.subheader("💬 Chat with Your Contracts")

        question = st.text_input(
            "Ask a question about your uploaded contracts"
        )

        if st.button("Ask Question"):

            if question.strip():

                try:

                    with st.spinner("Thinking..."):

                        st.session_state.chat_answer = chat_with_contract(
                            st.session_state.all_text,
                            question
                        )

                except Exception as e:

                    st.error(f"Chat failed: {str(e)}")

            else:

                st.warning("Please enter a question first.")

        if st.session_state.chat_answer:

            st.markdown("### 💡 Answer")

            st.write(st.session_state.chat_answer)


    # -----------------------------
    # SHARED MEMORY
    # -----------------------------
    with tabs[7]:

        st.subheader("🧠 Shared Agent Memory")

        memory = st.session_state.final_state.get(
            "shared_memory",
            []
        )

        if memory:

            st.write(memory)

        else:

            st.info("No shared memory available.")


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "ClauseAI © 2026 | LangGraph • Gemini • Pinecone • Streamlit"
)