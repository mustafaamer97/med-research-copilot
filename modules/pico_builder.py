import re


# ============================================================
# Search Term Extraction
# ============================================================

def extract_search_terms(text):
    """
    Extract meaningful search terms from a text string.
    Removes generic words that add little value to literature
    searches.
    """

    if not text:
        return []

    text = str(text).lower()

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
        "studies",
        "trial",
        "trials",
        "outcome",
        "outcomes",
        "the",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "to",
        "from",
        "between",
        "during",
        "year",
        "years",
        "rate",
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

    return list(dict.fromkeys(keywords))


# ============================================================
# Helpers
# ============================================================

def _clean_value(value):
    """Normalize empty / placeholder values."""

    if value is None:
        return ""

    value = str(value).strip()

    invalid_values = {
        "",
        "none",
        "null",
        "n/a",
        "na",
        "not applicable",
        "not specified",
        "no intervention",
        "no exposure",
        "none specified",
    }

    if value.lower() in invalid_values:
        return ""

    return value


def _requires_comparison(research_goal):
    """
    Determine whether comparison is conceptually important
    for the selected research goal.
    """

    return research_goal in {
        "Risk Factors",
        "Treatment Outcomes",
        "Diagnostic Accuracy",
        "Prediction Model",
    }


# ============================================================
# التعديل 1: دالة الكشف عن الدراسات الرصدية
# ============================================================

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


# ============================================================
# Research Question Builder
# ============================================================

def build_research_question(
    population,
    intervention,
    comparison,
    outcome,
    study_design="",
    research_goal="",
):
    """
    Generate a research question according to the research goal.

    Important:
    PICO is not always appropriate in the classical
    intervention-study sense. Epidemiological studies use
    adapted question structures.
    """

    population = _clean_value(population)
    intervention = _clean_value(intervention)
    comparison = _clean_value(comparison)
    outcome = _clean_value(outcome)
    study_design = _clean_value(study_design)
    research_goal = _clean_value(research_goal)

    # --------------------------------------------------------
    # Trend Analysis
    # --------------------------------------------------------

    if research_goal == "Trend Analysis":

        if intervention:
            question = (
                f"What were the temporal trends in {outcome} "
                f"among {population} according to {intervention}?"
            )
        else:
            question = (
                f"What were the temporal trends in {outcome} "
                f"among {population}?"
            )

        return question

    # --------------------------------------------------------
    # Incidence
    # --------------------------------------------------------

    if research_goal == "Incidence":

        question = (
            f"What was the incidence of {outcome} "
            f"among {population}?"
        )

        return question

    # --------------------------------------------------------
    # Prevalence
    # --------------------------------------------------------

    if research_goal == "Prevalence":

        question = (
            f"What was the prevalence of {outcome} "
            f"among {population}?"
        )

        return question

    # --------------------------------------------------------
    # التعديل 2: تحديث قسم Risk Factors بناءً على طبيعة الدراسة
    # --------------------------------------------------------

    if research_goal == "Risk Factors":
        observational = is_observational_design(
            study_design
        )
        if observational:
            if intervention and comparison:
                return (
                    f"Among {population}, is "
                    f"{intervention} associated with "
                    f"{outcome} compared with "
                    f"{comparison}?"
                )
            if intervention:
                return (
                    f"Among {population}, is "
                    f"{intervention} associated with "
                    f"{outcome}?"
                )
            return (
                f"What risk factors are associated "
                f"with {outcome} among {population}?"
            )
        else:
            if intervention and comparison:
                return (
                    f"In {population}, what is the effect "
                    f"of {intervention} compared with "
                    f"{comparison} on {outcome}?"
                )
            if intervention:
                return (
                    f"In {population}, what is the effect "
                    f"of {intervention} on {outcome}?"
                )
            return (
                f"What factors influence "
                f"{outcome} among {population}?"
            )

    # --------------------------------------------------------
    # Treatment Outcomes
    # --------------------------------------------------------

    if research_goal == "Treatment Outcomes":

        if intervention and comparison:

            return (
                f"Among {population}, what are the clinical "
                f"outcomes associated with {intervention} "
                f"compared with {comparison}?"
            )

        if intervention:

            return (
                f"Among {population}, what are the clinical "
                f"outcomes associated with {intervention}?"
            )

        return (
            f"What are the clinical outcomes among "
            f"{population}?"
        )

    # --------------------------------------------------------
    # Survival Analysis
    # --------------------------------------------------------

    if research_goal == "Survival Analysis":

        if intervention and comparison:

            return (
                f"Among {population}, what are the survival "
                f"outcomes associated with {intervention} "
                f"compared with {comparison}?"
            )

        if intervention:

            return (
                f"Among {population}, what factors, including "
                f"{intervention}, are associated with survival?"
            )

        return (
            f"What are the survival outcomes among "
            f"{population}?"
        )

    # --------------------------------------------------------
    # Diagnostic Accuracy
    # --------------------------------------------------------

    if research_goal == "Diagnostic Accuracy":

        if intervention and comparison:

            return (
                f"What is the diagnostic accuracy of "
                f"{intervention} compared with {comparison} "
                f"for detecting {outcome} among {population}?"
            )

        if intervention:

            return (
                f"What is the diagnostic accuracy of "
                f"{intervention} for detecting {outcome} "
                f"among {population}?"
            )

        return (
            f"What is the diagnostic accuracy for detecting "
            f"{outcome} among {population}?"
        )

    # --------------------------------------------------------
    # Prediction Model
    # --------------------------------------------------------

    if research_goal == "Prediction Model":

        if intervention:

            return (
                f"Can {outcome} be predicted among {population} "
                f"using {intervention}?"
            )

        return (
            f"Can {outcome} be predicted among "
            f"{population}?"
        )

    # --------------------------------------------------------
    # Systematic Review
    # --------------------------------------------------------

    if research_goal == "Systematic Review":

        if intervention and comparison:

            return (
                f"Among {population}, what is the effect of "
                f"{intervention} compared with {comparison} "
                f"on {outcome}?"
            )

        if intervention:

            return (
                f"What is the effect of {intervention} "
                f"on {outcome} among {population}?"
            )

        return (
            f"What is the available evidence regarding "
            f"{outcome} among {population}?"
        )

    # --------------------------------------------------------
    # Generic observational fallback
    # --------------------------------------------------------

    observational_designs = (
        "Cohort",
        "Case-Control",
        "Cross-Sectional",
        "Observational",
        "Registry",
        "Case Series",
    )

    if any(
        design_name.lower() in study_design.lower()
        for design_name in observational_designs
    ):

        if intervention and comparison:

            return (
                f"Among {population}, what is the association "
                f"between {intervention} and {outcome} "
                f"compared with {comparison}?"
            )

        if intervention:

            return (
                f"Among {population}, what is the association "
                f"between {intervention} and {outcome}?"
            )

        return (
            f"What is the occurrence of {outcome} "
            f"among {population}?"
        )

    # --------------------------------------------------------
    # Generic intervention fallback
    # --------------------------------------------------------

    if intervention and comparison:

        return (
            f"In {population}, what is the effect of "
            f"{intervention} compared with {comparison} "
            f"on {outcome}?"
        )

    if intervention:

        return (
            f"In {population}, what is the effect of "
            f"{intervention} on {outcome}?"
        )

    return (
        f"What is the relationship between {population} "
        f"and {outcome}?"
    )


# ============================================================
# Main PICO Builder
# ============================================================

def build_pico(
    population,
    intervention,
    comparison,
    outcome,
    study_design="",
    research_goal="",
    framework="PICO"
):
    """
    Build an adaptive research question and search strategy.

    This function remains backward-compatible with the existing
    Step 3 interface while adding research-goal-aware logic.
    """

    population = _clean_value(population)
    intervention = _clean_value(intervention)
    comparison = _clean_value(comparison)
    outcome = _clean_value(outcome)
    study_design = _clean_value(study_design)
    research_goal = _clean_value(research_goal)

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    missing = []

    if not population:
        missing.append("Population")

    if not outcome:
        missing.append("Outcome")

    if missing:

        return {
            "error": f"Missing: {', '.join(missing)}"
        }

    # --------------------------------------------------------
    # Remove inappropriate intervention/comparison
    # --------------------------------------------------------

    non_interventional_goals = {
        "Trend Analysis",
        "Incidence",
        "Prevalence",
        "Survival Analysis",
    }

    if research_goal in non_interventional_goals:

        if intervention.lower() in {
            "no intervention",
            "none",
            "not applicable",
            "not specified",
        }:
            intervention = ""

        if comparison.lower() in {
            "earlier years versus later years",
            "earlier years vs later years",
            "none",
            "not applicable",
            "not specified",
        }:
            comparison = ""

    # --------------------------------------------------------
    # التعديل 3: تحديد إطار العمل (PECO أو PICO) وتحديث الـ Return
    # --------------------------------------------------------

    pico_framework = framework

    # --------------------------------------------------------
    # Generate appropriate research question
    # --------------------------------------------------------

    question = build_research_question(
        population=population,
        intervention=intervention,
        comparison=comparison,
        outcome=outcome,
        study_design=study_design,
        research_goal=research_goal,
    )

    # --------------------------------------------------------
    # Search Terms
    # --------------------------------------------------------

    search_terms = []

    # Population is useful, but generic words are removed
    search_terms.extend(
        extract_search_terms(population)
    )

    # Add intervention/exposure only when meaningful
    if intervention:
        search_terms.extend(
            extract_search_terms(intervention)
        )

    # Add comparison only when meaningful
    if comparison and _requires_comparison(research_goal):
        search_terms.extend(
            extract_search_terms(comparison)
        )

    # Outcome is essential
    search_terms.extend(
        extract_search_terms(outcome)
    )

    # Remove duplicates
    search_terms = list(
        dict.fromkeys(search_terms)
    )

    # Limit query length
    keywords = " AND ".join(
        search_terms[:12]
    )

    # --------------------------------------------------------
    # Adaptive PICO
    # --------------------------------------------------------

    pico = {
        "population": population,
        "intervention": intervention,
        "comparison": comparison,
        "outcome": outcome,
    }

    return {
        "question": question,
        "keywords": keywords,
        "pico": pico,
        "framework": pico_framework,
        "framework_selected": pico_framework,
        "study_design": study_design,
        "research_goal": research_goal,
    }
