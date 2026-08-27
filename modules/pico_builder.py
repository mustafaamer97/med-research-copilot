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

    missing = []

    if not population:
        missing.append("Population")

    if not outcome:
        missing.append("Outcome")

    if missing:

        return {
            "error":
            f"Missing: {', '.join(missing)}"
        }

    # =========================
    # Adaptive Question
    # =========================

    if (
        any(
            x in study_design
            for x in [
                "Cohort",
                "Case-Control",
                "Cross-Sectional",
                "Observational",
                "Diagnostic",
                "Prognostic"
            ]
        )
    ):

        question = (
            f"Among {population}, "
            f"what is the relationship between "
            f"{intervention} and {outcome}"
        )

        if comparison:

            question += (
                f" compared with {comparison}"
            )

        question += "?"

    else:

        question = (
            f"In {population}, "
            f"does {intervention}"
        )

        if comparison:

            question += (
                f" compared with {comparison}"
            )

        question += (
            f" improve {outcome}?"
        )

    # =========================
    # Search Terms
    # =========================

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
        search_terms[:10]
    )

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
