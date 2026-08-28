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

    study_design = (
        research_context.get("recommended_design")
        or research_context.get("study_design")
        or ""
    )
    design_category = research_context.get(
        "design_category",
        ""
    )
    study_period = research_context.get(
        "study_period",
        ""
    )

    keywords = research_context.get(
        "keywords",
        ""
    )


    # =========================
    # Dynamic Evidence Search
    # =========================

    papers = get_recent_evidence(
        research_context
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

    # تم التحديث لتمرير research_context كاملاً كمعامل ثانٍ
    gap_report = detect_research_gaps(
        papers,
        research_context
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

Population:
{population}

Location:
{location}

Outcome:
{outcome}

Data Source:
{data_source}

Recommended Study Design:
{study_design}
Design Category:
{design_category}
Study Period:
{study_period}



Available Literature Evidence:

{evidence_text}



Research Gap Analysis:

{gap_text}



Generate exactly 5 research ideas.
For EACH idea return:
TITLE:
RATIONALE:
RESEARCH GAP:
POPULATION:
EXPOSURE_OR_INTERVENTION:
COMPARISON:
PRIMARY_OUTCOME:
SUGGESTED_STUDY_DESIGN:
EXPECTED_IMPACT:
FEASIBILITY_SCORE:
(0-100)
NOVELTY_SCORE:
(0-100)
PUBLICATION_POTENTIAL:
(0-100)


Rules:

- The study design must match the research goal.
- The study design must match the available data source.
- Do not force interventional designs.
- If the context suggests observational research, prefer observational ideas.
- If the context suggests evidence synthesis, prefer review ideas.
- If the context suggests diagnostic research, prefer diagnostic ideas.
- If the context suggests prognostic research, prefer prognostic ideas.
- If the context suggests prediction research, prefer prediction model ideas.
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
        user_input=f"{topic} {research_goal}"
    )


    return {
        "status": "success",
        "ideas": response,
        "topic": topic,
        "research_goal": research_goal,
        "study_design": study_design,
        "population": population,
        "outcome": outcome,
        "context": research_context,

        "evidence_count": len(papers),

        "gap_analysis": gap_report
    }
