# ==========================================
# Constants & Rule Engine Definitions
# ==========================================

COMPARATOR_REQUIRED_DESIGNS = {
    "Randomized",
    "Clinical Trial",
    "Case-Control",
    "Cohort",
    "Diagnostic",
    "Prediction"
}

VALID_DESIGNS_BY_DATA_SOURCE = {
    "Hospital Records": {
        "Cohort", "Longitudinal", "Prospective", "Retrospective",
        "Case-Control", "Cross-Sectional"
    },
    "Registry Database": {
        "Cohort", "Longitudinal", "Prospective", "Retrospective",
        "Case-Control", "Cross-Sectional"
    },
    "Electronic Health Records (EHR)": {
        "Cohort", "Longitudinal", "Prospective", "Retrospective",
        "Case-Control", "Cross-Sectional"
    },
    "Survey / Questionnaire": {
        "Cross-Sectional"
    },
    "Primary Data": {
        "Randomized", "Clinical Trial", "Adaptive", "Pragmatic",
        "Cohort", "Longitudinal", "Prospective", "Retrospective",
        "Case-Control", "Cross-Sectional", "Diagnostic"
    },
    "Published Literature": {
        "Systematic Review", "Meta-Analysis", "Scoping Review", "Umbrella Review"
    }
}

GOAL_RULES = {
    "Survival Analysis": {
        "required_designs": ["Survival", "Cohort"],
        "penalty": 10,
        "message": "Survival outcomes usually require longitudinal or time-to-event study designs."
    },
    "Prediction Model": {
        "required_designs": ["Prediction"],
        "penalty": 10,
        "message": "Prediction research usually requires model development or validation designs."
    },
    "Risk Factors": {
        "required_designs": ["Cohort", "Case-Control", "Cross-Sectional"],
        "penalty": 10,
        "message": "Risk factor studies require analytical observational designs."
    },
    "Diagnostic Accuracy": {
        "required_designs": ["Diagnostic"],
        "penalty": 10,
        "message": "Diagnostic studies usually require diagnostic accuracy designs."
    }
}


def score_to_level(score: int) -> str:
    """تحويل النتيجة الرقمية إلى مستوى تقييم نصوص."""
    if score >= 85:
        return "High"
    elif score >= 70:
        return "Moderate"
    return "Low"


# ==========================================
# Main Validation Functions
# ==========================================

def validate_research_idea(context: dict) -> dict:
    score = 100
    notes = []

    study_design = context.get("study_design", "")
    data_source = context.get("data_source", "")
    research_goal = context.get("research_goal", "")
    population = context.get("population", "")
    outcome = context.get("outcome", "")
    intervention = context.get("intervention", "")
    comparison = context.get("comparison", "")
    objective = context.get("objective", "")
    confidence = context.get("confidence", 100)

    # =========================
    # Confidence Penalty (Step 1 Integration)
    # =========================
    if confidence < 70:
        score -= 10
        notes.append("Research topic classification confidence is low.")

    # =========================
    # Study Design Feasibility
    # =========================
    if any(x in study_design for x in ["Randomized", "Clinical Trial", "Adaptive", "Pragmatic"]):
        score -= 25
        notes.append("Randomized studies require strong resources, ethical approval and controlled implementation.")
    elif any(x in study_design for x in ["Cohort", "Longitudinal", "Prospective", "Retrospective"]):
        score -= 10
        notes.append("Cohort studies require reliable follow-up data.")
    elif "Case-Control" in study_design:
        score -= 5
    elif any(x in study_design for x in ["Systematic Review", "Meta-Analysis", "Scoping Review", "Umbrella Review"]):
        score += 5

    # =========================
    # Data Source Compatibility & Design Validation
    # =========================
    if data_source in ["Hospital Records", "Registry Database", "Electronic Health Records (EHR)"]:
        score += 10
    elif data_source in ["Survey / Questionnaire", "Primary Data"]:
        score -= 10
        notes.append("Primary data collection increases time and operational requirements.")
    elif data_source == "Published Literature":
        score += 5

    # Check design compatibility with data source
    if data_source in VALID_DESIGNS_BY_DATA_SOURCE:
        valid_designs = VALID_DESIGNS_BY_DATA_SOURCE[data_source]
        if study_design and not any(design in study_design for design in valid_designs):
            score -= 20
            notes.append("Study design is incompatible with selected data source.")

    # =========================
    # Research Goal Compatibility (Rule Engine)
    # =========================
    if research_goal in GOAL_RULES:
        rule = GOAL_RULES[research_goal]
        if not any(req in study_design for req in rule["required_designs"]):
            score -= rule["penalty"]
            notes.append(rule["message"])

    if research_goal in ["Trend Analysis", "Incidence", "Prevalence"]:
        if data_source not in ["Registry Database", "Hospital Records", "Electronic Health Records (EHR)"]:
            score -= 15
            notes.append("Epidemiological trends require reliable population-level data.")

    # =========================
    # Completeness & PICO Evaluation
    # =========================
    if not population:
        score -= 5
        notes.append("Target population is not clearly defined.")

    if not outcome:
        score -= 10
        notes.append("Primary outcome should be specified.")

    if not intervention:
        score -= 5
        notes.append("Intervention/Exposure not specified.")

    if any(x in study_design for x in COMPARATOR_REQUIRED_DESIGNS):
        if not comparison:
            score -= 5
            notes.append("Comparator not specified.")

    if not objective:
        score -= 5
        notes.append("Study objective is not defined.")
    elif len(objective) < 20:
        score -= 5
        notes.append("Study objective appears too short.")

    # Full PICO check (Population, Intervention, Comparison, Outcome)
    pico_score = sum(1 for item in [population, intervention, comparison, outcome] if item)
    if pico_score < 3:
        score -= 10
        notes.append("PICO framework is incomplete.")

    # =========================
    # Final Score Normalization
    # =========================
    score = max(0, min(score, 100))
    feasibility = score_to_level(score)

    if score >= 90:
        notes.append("Research idea shows strong methodological compatibility.")

    return {
        "score": score,
        "feasibility": feasibility,
        "notes": notes,
        "validated": True
    }


def validate_idea_quality(context: dict) -> dict:
    result = validate_research_idea(context)
    score = result["score"]

    return {
        "feasibility": score,
        "novelty": None,
        "clinical_importance": None,
        "overall_score": score,
        "notes": result["notes"],
        "validated": True
    }


def validate_manual_idea(
    disease: str,
    outcome: str,
    description: str
) -> dict:
    score = 100
    notes = []

    if not disease:
        score -= 20
        notes.append("Disease or research topic is missing.")

    if not outcome:
        score -= 20
        notes.append("Main outcome is not specified.")

    if not description:
        score -= 20
        notes.append("Research description is incomplete.")
    elif len(description) < 50:
        score -= 10
        notes.append("Research description is too short.")

    score = max(0, score)
    quality = score_to_level(score)

    return {
        "overall_score": score,
        "quality": quality,
        "notes": notes,
        "validated": True
    }
