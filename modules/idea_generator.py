import streamlit as st

from ai.llm_engine import ask_ai
from ai.prompts import RESEARCH_IDEA_PROMPT

from modules.evidence_search import get_recent_evidence
from modules.research_gap_detector import detect_research_gaps


def generate_research_ideas(field):

    papers = get_recent_evidence(field)

    # تحليل الفجوات البحثية
    gap_report = detect_research_gaps(
        papers
    )

    evidence_text = ""

    for paper in papers:

        evidence_text += f"""

Title:
{paper.get('title', '')}

Journal:
{paper.get('journal', '')}

Publication Type:
{paper.get('publication_type', '')}

Evidence Level:
{paper.get('evidence_level', '')}

Abstract:
{paper.get('abstract', '')}

----------------------------------------

"""

    gap_text = f"""

Research Gap Analysis

Total Papers:
{gap_report['total_papers']}

Most Common Topics:
{gap_report['top_keywords']}

Most Common Study Types:
{gap_report['study_types']}

Most Common Journals:
{gap_report['top_journals']}

"""

    prompt = RESEARCH_IDEA_PROMPT.format(
        field=field
    )

    final_prompt = f"""

Evidence Context

{evidence_text}

{gap_text}

Instructions

Use ONLY the evidence above.

Identify:

1. Knowledge gaps
2. Under-studied topics
3. Missing populations
4. Missing outcomes
5. Missing methodologies

Generate realistic research ideas based on these gaps.

Do not invent references.

{prompt}

"""

    # Console Debug
    print("========== EVIDENCE ==========")
    print(evidence_text)

    print("========== GAP ANALYSIS ==========")
    print(gap_text)

    print("========== END ==========")

    # Debug داخل Streamlit
    with st.expander("Evidence Context"):

        st.write(evidence_text)

    with st.expander("Research Gap Analysis"):

        st.write(gap_text)

    return ask_ai(
        final_prompt,
        user_input=field
    )
