def is_observational_design(study_design):
    """
    Detect observational studies.
    """

    observational_keywords = [
        "cohort",
        "case-control",
        "cross-sectional",
        "observational",
        "registry",
        "case series",
        "prognostic",
        "prediction"
    ]

    study_design = str(study_design).lower()

    return any(
        keyword in study_design
        for keyword in observational_keywords
    )
