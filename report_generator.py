def generate_report(state, tone="professional", focus="balanced"):
    """
    Builds a readable final report from all agent outputs
    """

    sections = []

    # ---------------------------
    # HEADER
    # ---------------------------
    sections.append("CLAUSEAI AUTOMATED CONTRACT REPORT")
    sections.append("=" * 45)

    sections.append(f"Tone   : {tone.capitalize()}")
    sections.append(f"Focus  : {focus.capitalize()}")
    sections.append("")

    # ---------------------------
    # EXECUTIVE SUMMARY
    # ---------------------------
    sections.append("EXECUTIVE SUMMARY")
    sections.append("-" * 20)

    total_findings = (
        len(state["compliance"]) +
        len(state["finance"]) +
        len(state["legal"]) +
        len(state["operations"])
    )

    sections.append(
        f"This report analyzes the uploaded contract(s) and identified "
        f"{total_findings} significant clauses across compliance, finance, legal, "
        f"and operational domains. Each finding includes explanation, risk, "
        f"and suggested countermeasures."
    )

    sections.append("")

    # ---------------------------
    # HELPER FUNCTION
    # ---------------------------
    def add_section(title, findings):
        sections.append(f"\n{title.upper()}")
        sections.append("-" * len(title))

        if not findings:
            sections.append("No significant issues found.\n")
            return

        for idx, clause in enumerate(findings, 1):
            sections.append(f"\n{idx}. {clause.get('clause_type','N/A')}")
            sections.append(f"Explanation: {clause.get('explanation','')}")
            sections.append(f"How it appears: {clause.get('how_it_appears','')}")
            sections.append(f"Why it matters: {clause.get('why_it_matters','')}")
            sections.append(f"Risk: {clause.get('risk_or_note','')}")
            sections.append(
                f"Countermeasures: {clause.get('countermeasures','Not specified')}"
            )
            sections.append(f"Severity: {clause.get('severity','')}")
            sections.append(f"Source Document: {clause.get('source_document','')}")
            sections.append("")

    # ---------------------------
    # DOMAIN SECTIONS
    # ---------------------------
    add_section("Compliance Analysis", state["compliance"])
    add_section("Financial Analysis", state["finance"])
    add_section("Legal Analysis", state["legal"])
    add_section("Operational Analysis", state["operations"])

    # ---------------------------
    # RECOMMENDATIONS
    # ---------------------------
    sections.append("\nRECOMMENDATIONS")
    sections.append("-" * 15)

    sections.append(
        "Review high-severity clauses with legal counsel, clarify ambiguous language, "
        "add explicit countermeasures where missing, and ensure obligations are "
        "balanced between parties."
    )

    # ---------------------------
    # MEMORY LOG
    # ---------------------------
    sections.append("\nPROCESS NOTES")
    sections.append("-" * 12)

    if state.get("shared_memory"):
        for item in state["shared_memory"]:
            sections.append(f"- {item}")
    else:
        sections.append("No additional process notes.")

    return "\n".join(sections)
