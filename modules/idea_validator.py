def validate_research_idea(
    idea,
    context
):

    score = 100

    notes = []

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

    # =========================
    # Study Design Feasibility
    # =========================

    if any(
        x in study_design
        for x in [
            "Randomized",
            "Clinical Trial",
            "Adaptive",
            "Pragmatic"
        ]
    ):

        score -= 25

        notes.append(
            "Randomized studies require strong resources, ethical approval and controlled implementation."
        )

    elif any(
        x in study_design
        for x in [
            "Cohort",
            "Longitudinal",
            "Prospective",
            "Retrospective"
        ]
    ):

        score -= 10

        notes.append(
            "Cohort studies require reliable follow-up data."
        )

    elif "Case-Control" in study_design:

        score -= 5

    elif any(
        x in study_design
        for x in [
            "Systematic Review",
            "Meta-Analysis",
            "Scoping Review",
            "Umbrella Review"
        ]
    ):

        score += 5

    # =========================
    # Data Source Compatibility
    # =========================

    if data_source in [
        "Hospital Records",
        "Registry Database",
        "Electronic Health Records (EHR)"
    ]:

        score += 10

    elif data_source in [
        "Survey / Questionnaire",
        "Primary Data"
    ]:

        score -= 10

        notes.append(
            "Primary data collection increases time and operational requirements."
        )

    elif data_source == "Published Literature":

        score += 5

    # =========================
    # Study Design and Goal Compatibility
    # =========================

    if research_goal == "Survival Analysis":

        if "Survival" not in study_design and "Cohort" not in study_design:

            score -= 10

            notes.append(
                "Survival outcomes usually require longitudinal or time-to-event study designs."
            )

    if research_goal == "Prediction Model":

        if "Prediction" not in study_design:

            score -= 10

            notes.append(
                "Prediction research usually requires model development or validation designs."
            )

    if research_goal == "Risk Factors":

        if not any(
            x in study_design
            for x in [
                "Cohort",
                "Case-Control",
                "Cross-Sectional"
            ]
        ):

            score -= 10

            notes.append(
                "Risk factor studies require analytical observational designs."
            )

    # =========================
    # Research Goal Compatibility
    # =========================

    if research_goal in [
        "Trend Analysis",
        "Incidence",
        "Prevalence"
    ]:

        if data_source not in [
            "Registry Database",
            "Hospital Records",
            "Electronic Health Records (EHR)"
        ]:

            score -= 15

            notes.append(
                "Epidemiological trends require reliable population-level data."
            )

    if research_goal == "Diagnostic Accuracy":

        if "Diagnostic" not in study_design:

            notes.append(
                "Diagnostic studies usually require diagnostic accuracy designs."
            )

            score -= 10

    # =========================
    # Completeness
    # =========================

    if not population:

        score -= 5

        notes.append(
            "Target population is not clearly defined."
        )

    if not outcome:

        score -= 10

        notes.append(
            "Primary outcome should be specified."
        )

    if not context.get(
        "intervention"
    ):

        score -= 5

        notes.append(
            "Intervention/Exposure not specified."
        )

    comparison_required_designs = [
        "Randomized",
        "Clinical Trial",
        "Case-Control",
        "Cohort",
        "Diagnostic",
        "Prediction"
    ]

    if any(
        x in study_design
        for x in comparison_required_designs
    ):

        if not context.get(
            "comparison"
        ):

            score -= 5

            notes.append(
                "Comparator not specified."
            )

    if not context.get(
        "objective"
    ):

        score -= 5

        notes.append(
            "Study objective is not defined."
        )

    objective = context.get(
        "objective",
        ""
    )

    if objective and len(objective) < 20:

        score -= 5

        notes.append(
            "Study objective appears too short."
        )

    pico_score = 0

    for item in [
        context.get("population"),
        context.get("intervention"),
        context.get("outcome")
    ]:

        if item:

            pico_score += 1

    if pico_score < 3:

        score -= 10

        notes.append(
            "PICO framework is incomplete."
        )

    # =========================
    # Final Score
    # =========================

    score = max(
        0,
        min(
            score,
            100
        )
    )

    if score >= 85:

        feasibility = "High"

    elif score >= 70:

        feasibility = "Moderate"

    else:

        feasibility = "Low"

    if score >= 90:

        notes.append(
            "Research idea shows strong methodological compatibility."
        )

    return {

        "score":
        score,

        "feasibility":
        feasibility,

        "notes":
        notes,

        "validated":
        True

    }


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
        True
    }


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
        True
    }
