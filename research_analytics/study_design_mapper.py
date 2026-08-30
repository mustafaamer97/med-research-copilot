def get_recommended_statistics(
    study_design
):

    if "RCT" in study_design:

        return [
            "T-Test",
            "ANOVA",
            "Effect Size",
            "Intention-To-Treat"
        ]

    if "Cohort" in study_design:

        return [
            "Kaplan-Meier",
            "Cox Regression",
            "Hazard Ratio"
        ]

    if "Case-Control" in study_design:

        return [
            "Odds Ratio",
            "Chi-Square",
            "Logistic Regression"
        ]

    if "Cross-Sectional" in study_design:

        return [
            "Descriptive Statistics",
            "Chi-Square",
            "Logistic Regression"
        ]

    return [
        "Descriptive Statistics"
    ]
