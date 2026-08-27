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

    if "Randomized" in study_design:

        score -= 25

        notes.append(
            "Randomized studies require strong resources, ethical approval and controlled implementation."
        )


    elif "Cohort" in study_design:

        score -= 10

        notes.append(
            "Cohort studies require reliable follow-up data."
        )


    elif "Case-Control" in study_design:

        score -= 5


    elif "Systematic Review" in study_design:

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
