import streamlit as st

from ai.llm_engine import ask_ai

from modules.evidence_search import (
    get_recent_evidence
)

from modules.research_gap_detector import (
    detect_research_gaps
)


def generate_research_ideas(
    research_context
):

    # =========================
    # Extract Research Context
    # =========================

    topic = research_context.get(
        "research_topic",
        research_context.get(
            "disease",
            ""
        )
    )

    # التحقق من وجود المفهوم/المرض الأساسي
    if not topic:

        return {
            "status": "error",
            "message": "Research topic missing."
        }

    field = research_context.get(
        "field",
        research_context.get(
            "medical_field",
            ""
        )
    )

    research_goal = research_context.get(
        "research_goal",
        ""
    )

    population = research_context.get(
        "population",
        ""
    )

    location = research_context.get(
        "location",
        ""
    )

    outcome = research_context.get(
        "outcome",
        ""
    )

    data_source = research_context.get(
        "data_source",
        ""
    )

    study_design = research_context.get(
        "study_design",
        ""
    )

    keywords = research_context.get(
        "keywords",
        ""
    )


    # =========================
    # Dynamic Evidence Search
    # =========================

    query = f"""

    Topic:
    {topic}

    Field:
    {field}

    Goal:
    {research_goal}

    Outcome:
    {outcome}

    Population:
    {population}

    Keywords:
    {keywords}

    """


    papers = get_recent_evidence(
        query
    )


    if not papers:

        return {
            "status": "no_evidence",
            "ideas": [],
            "message":
            "No sufficient evidence found. Try broader keywords or modify the research topic."
        }


    # =========================
    # Gap Detection
    # =========================

    gap_report = detect_research_gaps(
        papers
    )


    evidence_text = ""


    for paper in papers[:20]:

        evidence_text += f"""

Title:
{paper.get('title','')}

Year:
{paper.get('year','')}

Study Type:
{paper.get('publication_type','')}

Evidence Level:
{paper.get('evidence_level','')}

Abstract:
{paper.get('abstract','')}

----------------------------

"""


    gap_text = f"""

Total Studies:
{gap_report.get('total_papers',0)}

Top Keywords:
{gap_report.get('top_keywords',[])}

Study Types:
{gap_report.get('study_types',[])}

Research Gaps:
{gap_report.get('research_gaps',[])}

"""


    # =========================
    # Research AI Prompt
    # =========================

    prompt = f"""

You are an expert medical research methodology advisor.

Your task is to generate feasible research ideas.

Research Context:

Topic:
{topic}

Medical Field:
{field}

Research Goal:
{research_goal}

Research Category:
{research_context.get('research_category','')}

Population:
{population}

Location:
{location}

Outcome:
{outcome}

Data Source:
{data_source}

Possible Study Design:
{study_design}



Available Literature Evidence:

{evidence_text}



Research Gap Analysis:

{gap_text}



Generate 5 research ideas.

For each idea provide:

1. Title

2. Rationale

3. Research Gap Addressed

4. Suggested Study Design

5. Target Population

6. Main Outcome

7. Expected Clinical/Public Health Impact


Rules:

- Adapt to any medical field.
- Do not assume oncology.
- Do not invent references.
- Do not invent PMID or DOI.
- Do not invent sample size.
- Do not invent statistical results.
- Prefer realistic studies based on available resources.
- Consider feasibility according to:
  - Available healthcare resources
  - Study location
  - Available data sources
  - Realistic recruitment possibilities
- Avoid suggesting studies that require unavailable technology or resources.


Return structured ideas.

"""


    with st.expander(
        "Evidence Used"
    ):

        st.text(
            evidence_text
        )


    with st.expander(
        "Research Gap Analysis"
    ):

        st.text(
            gap_text
        )


    response = ask_ai(
        prompt,
        user_input=topic
    )


    return {
        "status": "success",

        "ideas": response,

        "context": research_context,

        "evidence_count": len(papers),

        "gap_analysis": gap_report
    }
