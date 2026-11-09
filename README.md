CLAUSEAI – AI-Powered Contract Intelligence Platform
===================================================

ClauseAI is an AI-driven system designed to analyze legal contracts using
multi-agent reasoning, large language models, and vector databases.
The platform extracts, explains, and evaluates contract clauses across
multiple domains such as Compliance, Finance, Legal, and Operations.

---------------------------------------------------
PROJECT OBJECTIVE
---------------------------------------------------
The goal of ClauseAI is to help users:
- Understand complex legal clauses in simple language
- Identify risks and obligations in contracts
- Generate structured, domain-wise contract analysis
- Produce automated summaries and reports
- Interact with contracts using natural language queries

---------------------------------------------------
KEY FEATURES
---------------------------------------------------
1. Multi-Agent Contract Analysis
   - Specialized AI agents for:
     • Compliance
     • Finance
     • Legal
     • Operations
   - Each agent detects and explains relevant clauses

2. AI-Powered Clause Explanation
   - Uses Google Gemini LLM
   - Explains:
     • What the clause means
     • How it appears in the contract
     • Risks involved
     • Possible countermeasures

3. Vector-Based Clause Retrieval
   - Uses Pinecone Vector Database
   - Stores:
     • Contract chunks
     • Agent analysis outputs
     • Final reports
   - Enables semantic search and retrieval

4. Automated Report Generation
   - Generates structured contract reports
   - Customizable tone:
     • Professional
     • Business-friendly
     • Simple
     • Strict-legal
   - Customizable focus:
     • Balanced
     • Risk-heavy
     • Compliance-heavy
     • Financial-heavy

5. Parallel Contract Processing
   - Supports multiple contracts at once
   - Uses multithreading for faster indexing and analysis

6. Interactive Streamlit UI
   - Upload PDF and DOCX contracts
   - View extracted text
   - Explore agent-wise analysis
   - Generate and download final reports
   - Memory log to track agent decisions

7. Contract Memory & Traceability
   - Shared memory across agents
   - Tracks decisions, findings, and refinements
   - Stored for future reference and auditing

---------------------------------------------------
TECH STACK
---------------------------------------------------
Frontend:
- Streamlit

Backend / AI:
- Python
- LangGraph
- LangChain
- Google Gemini LLM

Vector Database:
- Pinecone

Embeddings:
- HuggingFace (all-MiniLM-L6-v2)

Document Processing:
- PyPDF2
- python-docx

---------------------------------------------------
PROJECT STRUCTURE
---------------------------------------------------
agents/           -> Domain-specific AI agents
graph/            -> LangGraph workflow definition
parser/           -> Contract document parsing
reports/          -> Automated report generation
utils/            -> LLM factory, vector store, utilities
app.py            -> Streamlit application entry point

---------------------------------------------------
WORKFLOW OVERVIEW
---------------------------------------------------
1. User uploads contract(s)
2. Contract text is extracted and indexed in Pinecone
3. Retrieval agent fetches relevant clauses
4. Domain agents analyze clauses in parallel
5. Refinement agent stores and consolidates results
6. Automated report is generated
7. Results are displayed in the UI

---------------------------------------------------
USE CASES
---------------------------------------------------
- Legal contract review
- Compliance checks
- Risk assessment
- Academic/legal research
- Contract understanding for non-legal users

---------------------------------------------------
CURRENT STATUS
---------------------------------------------------
- Core pipeline implemented
- Multi-agent analysis functional
- Report generation completed
- UI integrated
- Vector storage enabled

---------------------------------------------------
FUTURE ENHANCEMENTS
---------------------------------------------------
- Clause comparison across multiple contracts
- Chat-based contract Q&A
- PDF report export
- Role-based access
- Analytics dashboard

---------------------------------------------------
AUTHOR / CONTRIBUTION
---------------------------------------------------
This branch contains individual development work.
Main branch remains unchanged.

---------------------------------------------------
LICENSE
---------------------------------------------------
For academic and educational purposes.
