import hashlib
import json

from ai.llm_engine import ask_ai
from modules.evidence_search import get_recent_evidence
from modules.research_gap_detector import detect_research_gaps

# =========================
# Rule Engines & Knowledge Base
# =========================

GAP_TEMPLATES = {
    "Incidence": [
        "Limited regional incidence data in the target population.",
        "Lack of standardized registry-based estimates.",
        "Underrepresented regional populations in national reporting."
    ],
    "Prevalence": [
        "Limited regional prevalence data in the target population.",
        "Lack of standardized population-based prevalence estimates.",
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
    "Incidence": [
        "Estimate the baseline incidence of the condition.",
        "Describe temporal trends and demographic distribution."
    ],
    "Prevalence": [
        "Estimate the baseline prevalence of the condition.",
        "Describe sociodemographic and clinical distribution."
    ],
    "Risk Factors": [
        "Identify clinical, sociodemographic, and environmental predictors.",
        "Quantify adjusted risk estimates using multivariate analysis."
    ],
    "Treatment Outcomes": [
        "Evaluate therapeutic response and long-term clinical survival.",
        "Identify independent prognostic markers associated with complications."
    ],
    "Diagnostic Accuracy": [
        "Assess diagnostic sensitivity, specificity, and predictive values.",
        "Compare novel diagnostic indicators against standard gold references."
    ]
}

# Unified Data Source Names matching Step 1
ALLOWED_DESIGNS = {
    "Survey / Questionnaire": [
        "Cross-sectional Study", 
        "KAP (Knowledge, Attitudes, Practices) Study"
    ],
    "Hospital Records": [
        "Retrospective Cohort Study", 
        "Case-Control Study", 
        "Cross-sectional Study"
    ],
    "Electronic Health Records (EHR)": [
        "Retrospective Cohort Study", 
        "Case-Control Study", 
        "Cross-sectional Study"
    ],
    "Registry Database": [
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


def build_deterministic_meta(goal, population, design, outcome, topic=""):
    """
    Constructs accurate titles, questions, objectives, and PICO programmatically.
    Uses MD5 hashing for stable, reproducible gap selection across restarts.
    """
    gap_category = goal if goal in GAP_TEMPLATES else "Risk Factors"
    templates = GAP_TEMPLATES[gap_category]
    
    # MD5 hash-based deterministic selection for consistent output across restarts
    if topic:
        topic_hash = int(hashlib.md5(topic.lower().encode("utf-8")).hexdigest(), 16)
        gap_index = topic_hash % len(templates)
    else:
        gap_index = 0
        
    suggested_gap = templates[gap_index]
    
    # Professional Title Generator
    title = f"Predictors and Determinants of {outcome if outcome else 'Clinical Outcomes'} among {population}: A {design}"
    
    # Research Question
    research_question = f"What independent factors are significantly associated with {outcome if outcome else 'outcomes'} among {population} in this setting?"
    
    # Objectives
    objectives = OBJECTIVE_MAP.get(gap_category, [
        f"Assess primary rates of {outcome} in {population}.",
        f"Identify risk factors contributing to {outcome}."
    ])

    # PICO Framework
    pico = {
        "P": population,
        "I": "Primary exposure/risk factors under investigation",
        "C": "Non-exposed or standard control group",
        "O": outcome if outcome else "Primary clinical endpoints"
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
    Rule Filter: Checks design compatibility and tracks corrections.
    """
    if not data_source or data_source not in ALLOWED_DESIGNS:
        return study_design, False
    
    allowed = ALLOWED_DESIGNS[data_source]
    if study_design not in allowed:
        return allowed[0], True  # Auto-correct to first valid design
    return study_design, False


def build_fallback_ideas(meta, population, study_design, outcome, data_source):
    """
    Generates 3 robust deterministic fallback research ideas if LLM fails.
    """
    pico_obj = meta["pico"]
    
    return [
        {
            "id": 1,
            "title": meta["title"],
            "research_question": meta["research_question"],
            "rationale": "High-priority baseline epidemiological investigation tailored to local setting.",
            "research_gap": meta["suggested_gap"],
            "study_design": study_design,
            "target_population": population,
            "main_outcome": outcome,
            "objectives": meta["objectives"],
            "pico": pico_obj,
            "impact": "Establishes baseline evidence to inform local clinical decision-making.",
            "scores": {"novelty": 82, "feasibility": 92, "clinical_importance": 85, "overall": 86}
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
            "impact": "Enables targeted risk stratification and personalized patient care.",
            "scores": {"novelty": 85, "feasibility": 88, "clinical_importance": 87, "overall": 87}
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
            "impact": "Improves long-term patient survival outcomes and reduces disease burden.",
            "scores": {"novelty": 88, "feasibility": 84, "clinical_importance": 90, "overall": 87}
        }
    ]


def generate_research_ideas(research_context):
    """
    Pure Business Logic function to generate research ideas.
    Decoupled from Streamlit UI.
    """

    # Context Parsing & Verification
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
    raw_design = research_context.get("study_design", "Retrospective Cohort Study")
    keywords = research_context.get("keywords", "")
    confidence_level = research_context.get("confidence_level", "Moderate")

    # Data Source Compatibility Enforcement
    study_design, design_was_corrected = validate_design_against_datasource(raw_design, data_source)

    # Deterministic metadata base
    meta = build_deterministic_meta(research_goal, population, study_design, outcome, topic=topic)

    # Clean & Focused Query for Search Engine
    search_query = f"{topic} {outcome}".strip()
    papers = get_recent_evidence(search_query)

    if not papers:
        return {
            "status": "no_evidence",
            "ideas": [],
            "message": "No sufficient evidence found. Try broader keywords or modify the research topic."
        }

    gap_report = detect_research_gaps(papers)

    # Token Optimization: Top 10 papers metadata only
    evidence_text = ""
    for paper in papers[:10]:
        evidence_text += f"- Title: {paper.get('title','N/A')} | Year: {paper.get('year','N/A')} | Type: {paper.get('publication_type','N/A')}\n"

    # Robust handling for top_keywords (Strings or Tuples)
    raw_keywords = gap_report.get("top_keywords", [])
    formatted_keywords = [
        kw[0] if isinstance(kw, (tuple, list)) else str(kw)
        for kw in raw_keywords
    ]

    gap_text = f"""Total Studies: {gap_report.get('total_papers', 0)}
Top Keywords: {', '.join(formatted_keywords)}
Identified Gaps: {', '.join(gap_report.get('research_gaps', []))}
Sub-region Specific Gap: {meta['suggested_gap']}
"""

    # Format objectives & PICO cleanly for Prompt without json.dumps
    base_objectives_str = "\n".join([f"- {obj}" for obj in meta["objectives"]])
    base_pico_str = f"P: {meta['pico']['P']}\nI: {meta['pico']['I']}\nC: {meta['pico']['C']}\nO: {meta['pico']['O']}"

    # Prompt Setup
    prompt = f"""
You are an expert medical research methodology advisor.

Your task is to generate top 3 actionable, highly publishable research ideas derived strictly from the given user context and literature gaps.

CORE PARAMETERS (MUST COMPLY):
- Medical Field: {field}
- Topic/Condition: {topic} (Classification Confidence: {confidence_level})
- Research Goal: {research_goal}
- Target Population: {population}
- Primary Outcome: {outcome}
- Available Data Source: {data_source}
- Target Study Design: {study_design}
- Study Location: {location}

DETERMINISTIC BASELINES (USE & REFINE):
- Base Research Question: {meta['research_question']}
Base Objectives:
{base_objectives_str}
Base PICO Framework:
{base_pico_str}

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

RULES FOR THE 3 IDEAS:
- Idea 1 must focus on primary epidemiology/prevalence or baseline predictors.
- Idea 2 must focus on comparative risks or clinical subtypes.
- Idea 3 must focus on prognosis, survival, or long-term outcomes.
- Never invent PMIDs, DOIs, or fabricated statistical samples.
- Strictly keep designs practical for {location} using {data_source}.
"""

    response = ask_ai(prompt)

    # Parsing & Validation of JSON Output
    try:
        if isinstance(response, str):
            clean_json = response.strip().lstrip("```json").rstrip("```").strip()
            ideas_list = json.loads(clean_json)
        else:
            ideas_list = response

        # Enforce list type and strict length check (Must be at least 3 ideas)
        if not isinstance(ideas_list, list) or len(ideas_list) < 3:
            raise ValueError("LLM response did not contain at least 3 valid ideas.")

        ideas_list = ideas_list[:3]

    except Exception:
        # Fallback to 3 structured deterministic ideas on failure
        ideas_list = build_fallback_ideas(meta, population, study_design, outcome, data_source)

    return {
        "status": "success",
        "top_ideas": ideas_list,
        "context": research_context,
        "evidence_count": len(papers),
        "gap_analysis": gap_report,
        "deterministic_meta": meta,
        "design_corrected": design_was_corrected,
        "evidence_text": evidence_text,  # Clean UI pass-through
        "gap_text": gap_text            # Clean UI pass-through
    }
