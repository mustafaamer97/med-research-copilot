import json
import random
import streamlit as st

from ai.llm_engine import ask_ai
from modules.evidence_search import get_recent_evidence
from modules.research_gap_detector import detect_research_gaps

# =========================
# Rule Engines & Knowledge Base
# =========================

GAP_TEMPLATES = {
    "Incidence / Prevalence": [
        "Limited regional incidence/prevalence data in the target population.",
        "Lack of standardized registry-based estimates.",
        "Underrepresented regional populations in national reporting."
    ],
    "Risk Factors": [
        "Key clinical and environmental risk factors poorly characterized locally.",
        "Conflicting international evidence regarding primary determinants.",
        "Lack of multivariate risk prediction models tailored to local settings."
    ],
    "Treatment Outcomes": [
        "Long-term clinical and survival outcomes are poorly reported.",
        "Limited comparative effectiveness studies under real-world conditions.",
        "Scarcity of local data on therapy adherence and safety profiles."
    ],
    "Diagnostic Accuracy": [
        "Lack of validation for non-invasive diagnostic indicators locally.",
        "Limited head-to-head comparison between standard vs novelty tools."
    ]
}

OBJECTIVE_MAP = {
    "Incidence / Prevalence": [
        "Estimate the baseline incidence and prevalence of condition.",
        "Describe temporal trends and demographic distribution."
    ],
    "Risk Factors": [
        "Identify clinical, sociodemographic, and environmental predictors.",
        "Quantify adjusted risk estimates using multivariate analysis."
    ],
    "Treatment Outcomes": [
        "Evaluate therapeutic response and long-term clinical survival.",
        "Identify independent prognostic markers associated with complications."
    ]
}

# 8. Filter: Dynamic Data Source to Allowed Study Designs
ALLOWED_DESIGNS = {
    "Survey / Questionnaire": [
        "Cross-sectional Study", 
        "KAP (Knowledge, Attitudes, Practices) Study"
    ],
    "Medical Records / EMR": [
        "Retrospective Cohort Study", 
        "Case-Control Study", 
        "Cross-sectional Study"
    ],
    "Cancer Registry / Database": [
        "Retrospective Cohort Study", 
        "Survival Analysis", 
        "Incidence / Trend Analysis"
    ],
    "Clinical Trial / Prospective Data": [
        "Prospective Cohort Study", 
        "Randomized Controlled Trial (RCT)", 
        "Quasi-experimental Study"
    ]
}


def build_deterministic_meta(goal, population, design, outcome, data_source):
    """
    Constructs accurate titles, questions, objectives, and PICO programmatically.
    """
    # Fallback template gap
    gap_category = goal if goal in GAP_TEMPLATES else "Risk Factors"
    suggested_gap = random.choice(GAP_TEMPLATES[gap_category])
    
    # 4. Professional Title Generator
    title = f"Predictors and Determinants of {outcome if outcome else 'Clinical Outcomes'} among {population}: A {design}"
    
    # 5. Research Question
    research_question = f"What independent factors are significantly associated with {outcome if outcome else 'outcomes'} among {population} in this setting?"
    
    # 6. Objectives
    objectives = OBJECTIVE_MAP.get(gap_category, [
        f"Assess primary rates of {outcome} in {population}.",
        f"Identify risk factors contributing to {outcome}."
    ])

    # 7. PICO Framework
    pico = {
        "P (Population)": population,
        "I (Intervention / Exposure)": "Primary exposure/risk factors under investigation",
        "C (Comparison)": "Non-exposed or standard control group",
        "O (Outcome)": outcome if outcome else "Primary clinical endpoints"
    }

    return {
        "title": title,
        "suggested_gap": suggested_gap,
        "research_question": research_question,
        "objectives": objectives,
        "pico": pico
    }


def validate_design_against_datasource(study_design, data_source):
    """
    8. Rule Filter: Prevents incompatible designs (e.g. Survey vs Retrospective Cohort).
    """
    if not data_source or data_source not in ALLOWED_DESIGNS:
        return study_design
    
    allowed = ALLOWED_DESIGNS[data_source]
    if study_design not in allowed:
        return allowed[0] # Auto-correct to best valid design
    return study_design


def generate_research_ideas(research_context):

    # =========================
    # 2. Context Parsing & Verification
    # =========================
    topic = research_context.get("research_topic", research_context.get("disease", ""))

    if not topic:
        return {
            "status": "error",
            "message": "Research topic missing from Step 1 context."
        }

    field = research_context.get("field", research_context.get("medical_field", "General Medicine"))
    research_goal = research_context.get("research_goal", "Risk Factors")
    population = research_context.get("population", "Target Patients")
    location = research_context.get("location", "Local Health Centers")
    outcome = research_context.get("outcome", "Primary Endpoints")
    data_source = research_context.get("data_source", "Medical Records / EMR")
    raw_design = research_context.get("study_design", "Retrospective Cohort Study")
    keywords = research_context.get("keywords", "")

    # 8. Data Source Compatibility Enforcement
    study_design = validate_design_against_datasource(raw_design, data_source)

    # Deterministic metadata base
    meta = build_deterministic_meta(research_goal, population, study_design, outcome, data_source)

    # =========================
    # Dynamic Evidence Search & Gap Analysis
    # =========================
    search_query = f"{topic} {field} {population} {outcome} {keywords}".strip()
    papers = get_recent_evidence(search_query)

    if not papers:
        return {
            "status": "no_evidence",
            "ideas": [],
            "message": "No sufficient evidence found. Try broader keywords or modify the research topic."
        }

    gap_report = detect_research_gaps(papers)

    evidence_text = ""
    for paper in papers[:15]:
        evidence_text += f"""
Title: {paper.get('title','')}
Year: {paper.get('year','')}
Type: {paper.get('publication_type','')}
Abstract: {paper.get('abstract','')}
----------------------------
"""

    gap_text = f"""
Total Studies: {gap_report.get('total_papers',0)}
Top Keywords: {gap_report.get('top_keywords',[])}
Identified Gaps: {gap_report.get('research_gaps',[])}
Sub-region Specific Gap: {meta['suggested_gap']}
"""

    # =========================
    # 10. Top 3 Structured Ideas Prompt
    # =========================
    prompt = f"""
You are an expert medical research methodology advisor.

Your task is to generate top 3 actionable, highly publishable research ideas derived strictly from the given user context and literature gaps.

CORE PARAMETERS (MUST COMPLY):
- Medical Field: {field}
- Topic/Condition: {topic}
- Research Goal: {research_goal}
- Target Population: {population}
- Primary Outcome: {outcome}
- Available Data Source: {data_source}
- Target Study Design: {study_design}
- Study Location: {location}

LITERATURE EVIDENCE BASE:
{evidence_text}

GAP REPORT:
{gap_text}

EXPECTED OUTPUT FORMAT:
Return a valid JSON Array containing EXACTLY 3 objects (Top 3 Ideas). Do not add conversational text or markdown around JSON if possible.

Each object MUST contain:
1. "id": Integer (1, 2, or 3)
2. "title": String (Specific, publishable, standard medical journal format)
3. "research_question": String
4. "rationale": String
5. "research_gap": String
6. "study_design": String (Compatible with {data_source})
7. "target_population": String
8. "main_outcome": String
9. "objectives": List of Strings (2-3 items)
10. "pico": Object with keys ("P", "I", "C", "O")
11. "impact": String (Clinical or public health relevance)
12. "scores": Object containing:
    - "novelty": Int (0-100)
    - "feasibility": Int (0-100)
    - "clinical_importance": Int (0-100)
    - "overall": Int (Weighted score out of 100)

RULES:
- Idea 1 must focus on primary epidemiology/prevalence or predictors.
- Idea 2 must focus on comparative risks or clinical subtypes.
- Idea 3 must focus on prognosis, survival, or long-term outcomes.
- Never invent PMIDs, DOIs, or fabricated statistical samples.
- Strictly keep designs practical for {location} using {data_source}.
"""

    with st.expander("Evidence Used"):
        st.text(evidence_text)

    with st.expander("Research Gap Analysis"):
        st.text(gap_text)

    response = ask_ai(prompt, user_input=topic)

    # Parsing structured JSON output safely
    try:
        if isinstance(response, str):
            clean_json = response.strip().lstrip("```json").rstrip("```").strip()
            ideas_list = json.loads(clean_json)
        else:
            ideas_list = response
    except Exception:
        # Fallback if LLM output fails standard parsing
        ideas_list = [{
            "id": 1,
            "title": meta["title"],
            "research_question": meta["research_question"],
            "rationale": "High relevance study tailored to local health priority.",
            "research_gap": meta["suggested_gap"],
            "study_design": study_design,
            "target_population": population,
            "main_outcome": outcome,
            "objectives": meta["objectives"],
            "pico": meta["pico"],
            "impact": "Direct improvement in local evidence-based clinical decision making.",
            "scores": {"novelty": 85, "feasibility": 90, "clinical_importance": 88, "overall": 88}
        }]

    return {
        "status": "success",
        "top_ideas": ideas_list,
        "context": research_context,
        "evidence_count": len(papers),
        "gap_analysis": gap_report,
        "deterministic_meta": meta
    }
