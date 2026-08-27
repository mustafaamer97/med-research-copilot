import re


def extract_search_terms(text):

    if not text:
        return []

    text = text.lower()

    stop_words = {
        "with",
        "without",
        "compared",
        "comparison",
        "versus",
        "vs",
        "effect",
        "effects",
        "improve",
        "improves",
        "improved",
        "reduction",
        "increase",
        "decrease",
        "adults",
        "adult",
        "children",
        "child",
        "patients",
        "patient",
        "population",
        "group",
        "study",
        "trial",
        "outcome",
        "outcomes",
        "the",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "to"
    }

    words = re.findall(
        r"[a-zA-Z0-9\-]+",
        text
    )

    keywords = []

    for word in words:

        if len(word) < 3:
            continue

        if word in stop_words:
            continue

        keywords.append(word)

    return list(
        dict.fromkeys(keywords)
    )


def build_pico(
    population,
    intervention,
    comparison,
    outcome,
    study_design="",
    research_goal=""
):

    # =====================================
    # Validation
    # =====================================

    missing = []

    if not population.strip():
        missing.append("Population")

    if not outcome.strip():
        missing.append("Outcome")

    if missing:

        return {
            "error":
            f"Missing: {', '.join(missing)}"
        }

    study_design_str = (
        study_design or ""
    ).lower()

    research_goal_str = (
        research_goal or ""
    ).lower()

    # =====================================
    # Adaptive Medical Question Builder
    # =====================================

    # فحص الدراسات الرصدية مع التعامل المباشر مع حالات غياب الـ Intervention
    observational_study = any(
        x.lower() in study_design_str
        for x in [
            "cohort",
            "case-control",
            "cross-sectional",
            "observational",
            "diagnostic",
            "prognostic"
        ]
    )

    # =====================================
    # Survival Analysis
    # =====================================

    if (
        "survival" in research_goal_str
        or outcome.lower() == "survival"
    ):

        question = (
            f"What factors are associated with "
            f"survival among {population}?"
        )

    # =====================================
    # Risk Factors
    # =====================================

    elif (
        "risk" in research_goal_str
        or "risk factor" in research_goal_str
    ):

        question = (
            f"What are the risk factors among "
            f"{population}?"
        )

    # =====================================
    # Incidence
    # =====================================

    elif "incidence" in research_goal_str:

        question = (
            f"What is the incidence among "
            f"{population}?"
        )

    # =====================================
    # Prevalence
    # =====================================

    elif "prevalence" in research_goal_str:

        question = (
            f"What is the prevalence among "
            f"{population}?"
        )

    # =====================================
    # Observational Designs (Updated Logic)
    # =====================================

    elif observational_study:

        if intervention.strip():

            question = (
                f"Among {population}, "
                f"what is the relationship between "
                f"{intervention} and {outcome}"
            )

            if comparison.strip():

                question += (
                    f" compared with {comparison}"
                )

            question += "?"

        else:

            question = (
                f"What factors are associated with "
                f"{outcome.lower()} among "
                f"{population}?"
            )

    # =====================================
    # Interventional Designs
    # =====================================

    else:

        question = (
            f"In {population}, "
            f"does {intervention}"
        )

        if comparison.strip():

            question += (
                f" compared with {comparison}"
            )

        question += (
            f" improve {outcome}?"
        )

    # =====================================
    # Search Terms Extraction
    # =====================================

    search_terms = []

    for item in [
        population,
        intervention,
        comparison,
        outcome
    ]:

        search_terms.extend(
            extract_search_terms(item)
        )

    search_terms = list(
        dict.fromkeys(
            search_terms
        )
    )

    keywords = " AND ".join(
        search_terms[:15]
    )

    # =====================================
    # Return
    # =====================================

    return {

        "question":
        question,

        "keywords":
        keywords,

        "pico": {

            "population":
            population,

            "intervention":
            intervention,

            "comparison":
            comparison,

            "outcome":
            outcome
        },

        "study_design":
        study_design,

        "research_goal":
        research_goal
    }
