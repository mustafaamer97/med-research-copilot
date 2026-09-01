import json

from ai.llm_engine import ask_ai
from modules.evidence_search import get_recent_evidence
from modules.research_gap_detector import detect_research_gaps

# =========================
# Fallback Generation
# =========================

def build_fallback_ideas(population, study_design, outcome):
    """
    Generates 3 basic fallback research ideas if LLM fails.
    Removes mock scores as actual validation occurs in idea_validator.py.
    """
    pico_obj = {
        "P": population,
        "I": "Primary exposure/risk factors under investigation",
        "C": "Non-exposed or standard control group",
        "O": outcome if outcome else "Primary clinical endpoints"
    }
    
    return [
        {
            "id": 1,
            "title": f"Predictors and Determinants of {outcome} among {population}: A {study_design}",
            "research_question": f"What independent factors are significantly associated with {outcome} among {population}?",
            "rationale": "High-priority baseline epidemiological investigation tailored to local setting.",
            "research_gap": "Limited regional baseline epidemiological data in the target population.",
            "study_design": study_design,
            "target_population": population,
            "main_outcome": outcome,
            "objectives": [
                f"Assess primary rates of {outcome} in {population}.",
                f"Identify risk factors contributing to {outcome}."
            ],
            "pico": pico_obj,
            "impact": "Establishes baseline evidence to inform local clinical decision-making."
        },
        {
            "id": 2,
            "title": f"Comparative Risk Assessment of {outcome} Subtypes in {population}",
            "research_question": f"How do demographic and clinical subgroups differ regarding {outcome} risk in {population}?",
            "rationale": "Comparative risk analysis identifies high-risk clinical sub-populations.",
            "research_gap": "Lack of comparative subgroup stratification studies in the region.",
            "study_design": study_design,
            "target_population": population,
            "main_outcome": outcome,
            "objectives": [
                f"Stratify {population} into distinct risk subgroups.",
                f"Compare the odds of {outcome} across subgroups using multivariate modeling."
            ],
            "pico": pico_obj,
            "impact": "Enables targeted risk stratification and personalized patient care."
        },
        {
            "id": 3,
            "title": f"Prognostic Indicators and Long-term {outcome} in {population}: A {study_design}",
            "research_question": f"What prognostic markers are predictive of long-term {outcome} in {population}?",
            "rationale": "Evaluating prognosis assists clinicians in long-term management and intervention planning.",
            "research_gap": "Scarcity of long-term prognostic and clinical trajectory data in local health centers.",
            "study_design": study_design,
            "target_population": population,
            "main_outcome": outcome,
            "objectives": [
                f"Track long-term trajectory of {outcome} in {population}.",
                "Identify independent prognostic markers for early clinical intervention."
            ],
            "pico": pico_obj,
            "impact": "Improves long-term patient survival outcomes and reduces disease burden."
        }
    ]


# =========================
# Core Generator Flow
# =========================

def generate_research_ideas(research_context):
    """
    Pure Generation Flow:
    Context -> Evidence Search -> Gap Detection -> AI Generation -> Top 3 Ideas
    """
    # 1. Context Parsing
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
    data_source = research_context.get("data_source", "Hospital Records")
    study_design = research_context.get("study_design", "Retrospective Cohort Study")

    # 2. Evidence Search
    search_query = f"{topic} {outcome}".strip()
    papers = get_recent_evidence(search_query)

    if not papers:
        return {
            "status": "no_evidence",
            "ideas": [],
            "message": "No sufficient evidence found. Try broader keywords or modify the research topic."
        }

    # 3. Gap Detection
    gap_report = detect_research_gaps(papers)

    evidence_text = ""
    for paper in papers[:10]:
        evidence_text += f"- Title: {paper.get('title','N/A')} | Year: {paper.get('year','N/A')} | Type: {paper.get('publication_type','N/A')}\n"

    raw_keywords = gap_report.get("top_keywords", [])
    formatted_keywords = [
        kw[0] if isinstance(kw, (tuple, list)) else str(kw)
        for kw in raw_keywords
    ]

    gap_text = f"""Total Studies: {gap_report.get('total_papers', 0)}
Top Keywords: {', '.join(formatted_keywords)}
Identified Gaps: {', '.join(gap_report.get('research_gaps', []))}
"""

    # 4. AI Generation Prompt
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
Return a valid JSON Array containing EXACTLY 3 objects (Top 3 Ideas). Do not add conversational text or markdown around JSON.

Each object MUST contain:
1. "id": Integer (1, 2, or 3)
2. "title": String (Specific, publishable, standard medical journal format)
3. "research_question": String
4. "rationale": String
5. "research_gap": String
6. "study_design": String
7. "target_population": String
8. "main_outcome": String
9. "objectives": List of Strings (2-3 items)
10. "pico": Object with keys ("P", "I", "C", "O")
11. "impact": String (Clinical or public health relevance)

RULES FOR THE 3 IDEAS:
- Idea 1 must focus on primary epidemiology/prevalence or baseline predictors.
- Idea 2 must focus on comparative risks or clinical subtypes.
- Idea 3 must focus on prognosis, survival, or long-term outcomes.
- Never invent PMIDs, DOIs, or fabricated statistical samples.
- Strictly keep designs practical for {location} using {data_source}.
"""

    response = ask_ai(prompt)

    # 5. Parsing Output & Fallback Handling
    try:
        if isinstance(response, str):
            clean_json = response.strip().lstrip("```json").rstrip("```").strip()
            ideas_list = json.loads(clean_json)
        else:
            ideas_list = response

        if not isinstance(ideas_list, list) or len(ideas_list) < 3:
            raise ValueError("LLM response did not contain at least 3 valid ideas.")

        ideas_list = ideas_list[:3]

    except Exception:
        ideas_list = build_fallback_ideas(population, study_design, outcome)

    # 6. Clean Return Payload
    return {
        "status": "success",
        "top_ideas": ideas_list,
        "evidence_count": len(papers),
        "gap_analysis": gap_report
    }
