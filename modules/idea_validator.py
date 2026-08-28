# ============================================================
# Research Context Validator
# ============================================================

def validate_research_idea(
    idea,
    context
):

    context = context or {}

    score = 100

    notes = []

    topic = (
        context.get("research_topic")
        or context.get("disease")
        or idea
        or ""
    )

    study_design = context.get(
        "study_design",
        ""
    )

    data_source = context.get(
        "data_source",
        ""
    )

    research_goal = context.get(
        "research_goal",
        ""
    )

    population = context.get(
        "population",
        ""
    )

    outcome = context.get(
        "outcome",
        ""
    )

    location = context.get(
        "location",
        ""
    )

    study_period = (
        context.get("study_period")
        or context.get("period")
        or ""
    )

    keywords = context.get(
        "keywords",
        ""
    )

    # ========================================================
    # Required Context
    # ========================================================

    if not topic.strip():

        score -= 20

        notes.append(
            "Research topic is not clearly defined."
        )

    if not population.strip():

        score -= 10

        notes.append(
            "Target population is not clearly defined."
        )

    if not outcome.strip():

        score -= 10

        notes.append(
            "Primary outcome should be specified."
        )

    if not location.strip():

        score -= 5

        notes.append(
            "Study location or setting is missing."
        )

    if not study_period.strip():

        score -= 5

        notes.append(
            "Study period is missing."
        )

    if not str(keywords).strip():

        score -= 5

        notes.append(
            "Research keywords are missing."
        )

    # ========================================================
    # Study Design Feasibility
    # ========================================================

    if any(
        x in study_design
        for x in [
            "Randomized",
            "Clinical Trial",
            "Adaptive",
            "Pragmatic",
        ]
    ):

        score -= 20

        notes.append(
            "Interventional studies require adequate resources, "
            "ethical approval, recruitment and controlled implementation."
        )

    elif any(
        x in study_design
        for x in [
            "Cohort",
            "Longitudinal",
            "Prospective",
            "Retrospective",
        ]
    ):

        score -= 5

        notes.append(
            "Cohort studies require reliable participant or follow-up data."
        )

    elif "Case-Control" in study_design:

        score -= 3

    elif any(
        x in study_design
        for x in [
            "Systematic Review",
            "Meta-Analysis",
            "Scoping Review",
            "Umbrella Review",
        ]
    ):

        score += 5

    # ========================================================
    # Data Source Compatibility
    # ========================================================

    if data_source in [
        "Hospital Records",
        "Registry Database",
        "Electronic Health Records (EHR)",
    ]:

        score += 10

    elif data_source in [
        "Survey / Questionnaire",
        "Primary Data",
    ]:

        score -= 5

        notes.append(
            "Primary data collection increases operational requirements."
        )

    elif data_source == "Published Literature":

        score += 5

    # ========================================================
    # Goal / Design Compatibility
    # ========================================================

    if research_goal == "Survival Analysis":

        if not any(
            x in study_design
            for x in [
                "Survival",
                "Cohort",
                "Prognostic",
            ]
        ):

            score -= 10

            notes.append(
                "Survival analysis usually requires longitudinal "
                "or time-to-event data."
            )

    if research_goal == "Prediction Model":

        if "Prediction" not in study_design:

            score -= 10

            notes.append(
                "Prediction research usually requires a prediction "
                "model development or validation design."
            )

    if research_goal == "Risk Factors":

        if not any(
            x in study_design
            for x in [
                "Cohort",
                "Case-Control",
                "Cross-Sectional",
            ]
        ):

            score -= 10

            notes.append(
                "Risk-factor research usually requires an analytical "
                "observational design."
            )

    if research_goal in [
        "Trend Analysis",
        "Incidence",
        "Prevalence",
    ]:

        if data_source not in [
            "Registry Database",
            "Hospital Records",
            "Electronic Health Records (EHR)",
        ]:

            score -= 10

            notes.append(
                "Incidence, prevalence and trend analyses require "
                "reliable population or healthcare data."
            )

    if research_goal == "Diagnostic Accuracy":

        if "Diagnostic" not in study_design:

            score -= 10

            notes.append(
                "Diagnostic accuracy research should use an appropriate "
                "diagnostic study design."
            )

    # ========================================================
    # Design / Data Source Conflict
    # ========================================================

    if (
        data_source == "Published Literature"
        and study_design
        not in [
            "Systematic Review",
            "Meta-Analysis",
            "Network Meta-Analysis",
            "Scoping Review",
            "Umbrella Review",
        ]
    ):

        score -= 15

        notes.append(
            "Published literature as the primary data source is generally "
            "more compatible with evidence-synthesis designs."
        )

    # ========================================================
    # Final Score
    # ========================================================

    score = max(
        0,
        min(
            int(score),
            100
        )
    )

    if score >= 85:

        feasibility = "High"

    elif score >= 70:

        feasibility = "Moderate"

    else:

        feasibility = "Low"

    if not notes:

        notes.append(
            "Research context shows good methodological compatibility."
        )

    return {

        "score":
        score,

        "feasibility":
        feasibility,

        "notes":
        notes,

        "validated":
        True,
    }


# ============================================================
# Idea Quality Validator
# ============================================================

def validate_idea_quality(
    context,
    idea
):

    result = validate_research_idea(
        idea,
        context
    )

    score = result["score"]

    return {

        "feasibility":
        score,

        "novelty":
        score,

        "clinical_importance":
        score,

        "overall_score":
        score,

        "notes":
        result["notes"],

        "validated":
        True,
    }


# ============================================================
# Manual Idea Validator
# ============================================================

def validate_manual_idea(
    disease,
    outcome,
    description
):

    score = 100

    notes = []

    if not disease:

        score -= 20

        notes.append(
            "Disease or research topic is missing."
        )

    if not outcome:

        score -= 20

        notes.append(
            "Main outcome is not specified."
        )

    if not description:

        score -= 20

        notes.append(
            "Research description is incomplete."
        )

    score = max(
        0,
        score
    )

    if score >= 85:

        quality = "High"

    elif score >= 70:

        quality = "Moderate"

    else:

        quality = "Low"

    return {

        "overall_score":
        score,

        "quality":
        quality,

        "notes":
        notes,

        "validated":
        True,
    }
