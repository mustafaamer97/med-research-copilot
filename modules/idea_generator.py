import streamlit as st

from ai.llm_engine import ask_ai
from ai.prompts import RESEARCH_IDEA_PROMPT

from modules.evidence_search import get_recent_evidence
from modules.research_gap_detector import detect_research_gaps


def generate_research_ideas(field):

    # =========================
    # Fetch Evidence
    # =========================

    papers = get_recent_evidence(field)

    if not papers:

        return """
FACTS
No PubMed evidence was retrieved.

ASSUMPTIONS
None.

LIMITATIONS
Unable to generate evidence-based ideas.
"""

    # =========================
    # Gap Analysis
    # =========================

    gap_report = detect_research_gaps(
        papers
    )

    # =========================
    # Evidence Context
    # =========================

    evidence_text = ""

    for paper in papers:

        evidence_text += f"""

Title:
{paper.get("title", "")}

Journal:
{paper.get("journal", "")}

Publication Type:
{paper.get("publication_type", "")}

Evidence Level:
{paper.get("evidence_level", "Unknown")}

Publication Date:
{paper.get("publication_date", "")}

Year:
{paper.get("year", "")}

PMID:
{paper.get("pmid", "")}

DOI:
{paper.get("doi", "")}

Country:
{paper.get("country", "")}

Language:
{paper.get("language", "")}

MeSH Terms:
{paper.get("mesh_terms", "")}

Abstract:
{paper.get("abstract", "")}

--------------------------------------------------

"""

    # =========================
    # Gap Report
    # =========================

    gap_text = f"""

Research Gap Analysis

Total Papers:
{gap_report.get("total_papers", 0)}

Most Common Topics:
{gap_report.get("top_keywords", [])}

Most Common Study Types:
{gap_report.get("study_types", [])}

Most Common Journals:
{gap_report.get("top_journals", [])}

Most Common Countries:
{gap_report.get("top_countries", [])}

Most Common MeSH Terms:
{gap_report.get("top_mesh_terms", [])}

"""

    # =========================
    # Build Prompt
    # =========================

    prompt = RESEARCH_IDEA_PROMPT.format(
        field=field
    )

    final_prompt = f"""

Evidence Context

{evidence_text}

==================================================

{gap_text}

==================================================

Instructions

You are a medical research advisor.

Use ONLY the evidence provided above.

Prioritize findings coming from:

- Level 1 Evidence
- Level 2 Evidence

Before using lower-level evidence.

Identify:

1. Knowledge Gaps
2. Under-studied Populations
3. Under-studied Outcomes
4. Missing Methodologies
5. Future Research Opportunities

Generate 5 high-quality research ideas.

For each idea provide:

- Title
- Rationale
- Potential Study Design
- Suggested Population
- Expected Clinical Impact

Do NOT invent:

- References
- DOI
- PMID
- Statistical Results
- Sample Sizes
- Study Findings not present in the evidence

Base your suggestions ONLY on the supplied evidence.

{prompt}

"""

    # =========================
    # Debug Console
    # =========================

    print("========== EVIDENCE ==========")
    print(evidence_text)

    print("========== GAP ANALYSIS ==========")
    print(gap_text)

    print("========== END ==========")

    # =========================
    # Streamlit Debug View
    # =========================

    with st.expander("PubMed Evidence"):

        st.text(evidence_text)

    with st.expander("Research Gap Analysis"):

        st.text(gap_text)

    # =========================
    # Generate Ideas
    # =========================

    return ask_ai(
        final_prompt,
        user_input=field
    )
