def detect_research_type(
    disease,
    outcome,
    data_source,
):
    disease_lower = disease.lower()
    outcome_lower = outcome.lower()

    field = "General Medicine"

    if any(
        x in disease_lower
        for x in [
            "cancer",
            "tumor",
            "oncology",
            "neoplasm",
            "leukemia",
            "lymphoma",
        ]
    ):
        field = "Oncology"

    elif any(
        x in disease_lower
        for x in [
            "heart",
            "cardiac",
            "cardiology",
            "myocardial",
        ]
    ):
        field = "Cardiology"

    elif any(
        x in disease_lower
        for x in [
            "stroke",
            "brain",
            "neurology",
            "epilepsy",
        ]
    ):
        field = "Neurology"

    elif any(
        x in disease_lower
        for x in [
            "diabetes",
            "endocrine",
            "thyroid",
        ]
    ):
        field = "Endocrinology"

    population = "General Population"

    if field == "Oncology":
        population = (
            "Patients diagnosed with malignant neoplasms"
        )

    recommended_design = (
        "Cross-Sectional Study"
    )

    if any(
        x in outcome_lower
        for x in [
            "trend",
            "incidence",
            "prevalence",
            "distribution",
        ]
    ):

        if data_source in [
            "Registry Database",
            "Hospital Records",
            "EHR",
        ]:

            recommended_design = (
                "Retrospective Registry-Based Study"
            )

    keywords = []

    if field == "Oncology":

        keywords = [
            disease,
            "Cancer",
            "Neoplasm",
            "Incidence",
            "Trend",
            "Registry",
            "Epidemiology",
        ]

    return {
        "field": field,
        "population": population,
        "recommended_design":
        recommended_design,
        "keywords": keywords,
    }
