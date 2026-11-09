# utils/llm_factory.py

import os
import google.generativeai as genai

# -----------------------------------------
# CONFIGURE GEMINI
# -----------------------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# -----------------------------------------
# GEMINI WRAPPER
# -----------------------------------------
class GeminiLLM:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # -----------------------------
    # Core call
    # -----------------------------
    def ask(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"LLM Error: {str(e)}"

    # -----------------------------
    # Backward Compatibility
    # -----------------------------
    def invoke(self, messages):
        if isinstance(messages, str):
            return self.ask(messages)

        if isinstance(messages, list):
            prompt = "\n".join(m.content for m in messages)
            return self.ask(prompt)

        raise ValueError("Unsupported input type for LLM")

    # -----------------------------
    # Clause Summary
    # -----------------------------
    def summarize_clause(self, clause_text):
        prompt = f"""
Summarize the following contract clause in plain English.

Clause:
{clause_text}

Write 4-5 short sentences.
"""
        return self.ask(prompt)

    # -----------------------------
    # Clause Explanation
    # -----------------------------
    def explain_clause(self, clause_type, clause_text):
        prompt = f"""
You are a legal assistant.

Explain the {clause_type} below:

{clause_text}

Include:
- What it means
- How it works in this contract
- Main risk
- How to reduce the risk

Write in simple language.
"""
        return self.ask(prompt)

    # -----------------------------
    # Risk Scoring
    # -----------------------------
    def score_risk(self, clause_text):
        prompt = f"""
Give a risk score between 1 (low) and 10 (high) for this clause:

{clause_text}

Only return a number.
"""
        return self.ask(prompt)

    # -----------------------------
    # Report Section Generator
    # -----------------------------
    def generate_report_section(self, title, findings):
        text = f"{title}\n" + "-" * len(title) + "\n"

        if not findings:
            return text + "No major issues found.\n\n"

        for f in findings:
            text += f"""
Clause: {f['clause_type']}
Summary: {f.get('summary')}
Risk: {f.get('risk_score')}
Source: {f.get('source_document')}
"""
        return text

    # -----------------------------
    # Chat Support (future)
    # -----------------------------
    def chat(self, history, user_input):
        prompt = "Conversation so far:\n"

        for h in history:
            prompt += f"{h['role']}: {h['content']}\n"

        prompt += f"\nUser: {user_input}\nAssistant:"

        return self.ask(prompt)


# -----------------------------------------
# Factory
# -----------------------------------------
def get_llm():
    return GeminiLLM()

