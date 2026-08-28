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


# =====================================
# التعديل 1: Framework Detector
# =====================================
def detect_framework(
    study_design=""
):
    design = (
        study_design or ""
    ).lower()
    if "systematic review" in design:
        return "PEO"
    if "meta-analysis" in design:
        return "PEO"
    if "diagnostic" in design:
        return "PIRT"
    if "prognostic" in design:
        return "PICOTS"
    if "prediction" in design:
        return "PICOTS"
    if "cross-sectional" in design:
        return "PEO"
    if "case-control" in design:
        return "PEO"
    if "cohort" in design:
        return "PEO"
    return "PICO"


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
    # التعديل 2: تحديد الـ Framework
    # =====================================
    framework = detect_framework(
        study_design
    )

    # =====================================
    # التعديل 3: Dynamic Framework Builder
    # =====================================
    if framework == "PICO":
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
    elif framework == "PEO":
        if intervention.strip():
            question = (
                f"Among {population}, "
                f"is {intervention} associated with "
                f"{outcome}?"
            )
        else:
            question = (
                f"What factors are associated with "
                f"{outcome} among "
                f"{population}?"
            )
    elif framework == "PIRT":
        question = (
            f"How accurately does "
            f"{intervention} diagnose "
            f"{outcome} among "
            f"{population}?"
        )
    elif framework == "PICOTS":
        if "prediction" in study_design_str:
            question = (
                f"Can a prediction model estimate "
                f"{outcome} among "
                f"{population}?"
            )
        else:
            question = (
                f"What prognostic factors predict "
                f"{outcome} among "
                f"{population}?"
            )
    else:
        question = (
            f"What is the relationship between "
            f"{intervention} and {outcome} "
            f"among {population}?"
        )

    # =====================================
    # التعديل 4: دعم Survival و Prognostic بشكل أفضل
    # =====================================
    if (
        "survival" in research_goal_str
        or
        "mortality" in outcome.lower()
    ):
        question = (
            f"What factors are associated with "
            f"survival among "
            f"{population}?"
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

    # =====================================
    # التعديل 5: تحسين كلمات البحث
    # =====================================
    if study_design:
        search_terms.append(
            study_design
        )
    keywords = " AND ".join(
        list(
            dict.fromkeys(
                search_terms
            )
        )[:20]
    )

    # =====================================
    # Return (تعديلات 6، 7، 8)
    # =====================================

    return {

        "question":
        question,

        "keywords":
        keywords,

        "framework":
        framework,

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

        "recommended_study_design":
        study_design,

        "research_goal":
        research_goal
    }
