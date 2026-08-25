def validate_research_idea(
    study_design,
    data_source
):

    score = 100

    notes = []

    # Study Design

    if study_design == "Randomized Controlled Trial (RCT)":

        score -= 35

        notes.append(
            "RCT requires substantial resources and ethics approval."
        )

    elif study_design == "Cohort Study":

        score -= 15

    elif study_design == "Case-Control Study":

        score -= 10

    elif study_design == "Cross-Sectional Study":

        score -= 0

    elif study_design == "Systematic Review":

        score -= 5

    # Data Source

    if data_source == "Primary Data":

        score -= 20

        notes.append(
            "Primary data collection may require more time and approvals."
        )

    elif data_source == "Hospital Records":

        score -= 5

    elif data_source == "Literature Only":

        score += 0

    # Classification

    if score >= 85:

        feasibility = "High"

    elif score >= 70:

        feasibility = "Moderate"

    else:

        feasibility = "Low"

    return {
        "score": score,
        "feasibility": feasibility,
        "notes": notes
    }
