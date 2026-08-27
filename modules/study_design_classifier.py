import re


# ============================================================
# Study Design Classifier
# ============================================================

DESIGN_TYPES = {
    "retrospective_observational": "Retrospective Observational Study",
    "retrospective_cohort": "Retrospective Cohort Study",
    "prospective_cohort": "Prospective Cohort Study",
    "cross_sectional": "Cross-Sectional Study",
    "case_control": "Case-Control Study",
    "randomized_controlled_trial": "Randomized Controlled Trial",
    "clinical_trial": "Clinical Trial",
    "diagnostic_accuracy": "Diagnostic Accuracy Study",
    "systematic_review": "Systematic Review",
    "meta_analysis": "Systematic Review and Meta-analysis",
    "ecological": "Ecological Study",
    "descriptive": "Descriptive Epidemiological Study",
    "prognostic": "Prognostic Study",
}


# ============================================================
# Helpers
# ============================================================

def _clean(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def _contains_any(text, keywords):

    text = _clean(text)

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def _score_design(scores, design, points, reason):

    scores.setdefault(
        design,
        {
            "score": 0,
            "reasons": []
        }
    )

    scores[design]["score"] += points

    if reason:
        scores[design]["reasons"].append(reason)


# ============================================================
# Main Classifier
# ============================================================

def classify_study_design(
    research_goal="",
    data_source="",
    collection_method="",
    population="",
    intervention="",
    comparison="",
    outcome="",
    study_period="",
    sampling_method="",
    research_question="",
    topic="",
):
    """
    Automatically recommends the most appropriate study design.

    Returns:
        {
            "recommended_design": str,
            "design_category": str,
            "confidence": int,
            "score": int,
            "reasons": list,
            "alternatives": list,
            "warnings": list
        }
    """

    goal = _clean(research_goal)
    source = _clean(data_source)
    method = _clean(collection_method)
    pop = _clean(population)
    intervention_text = _clean(intervention)
    comparison_text = _clean(comparison)
    outcome_text = _clean(outcome)
    period = _clean(study_period)
    sampling = _clean(sampling_method)
    question = _clean(research_question)
    topic_text = _clean(topic)

    combined = " ".join([
        goal,
        source,
        method,
        pop,
        intervention_text,
        comparison_text,
        outcome_text,
        period,
        sampling,
        question,
        topic_text,
    ])

    scores = {}

    # ========================================================
    # 1. Systematic Review / Meta-analysis
    # ========================================================

    if _contains_any(
        combined,
        [
            "systematic review",
            "systematic literature review",
            "meta-analysis",
            "meta analysis",
            "literature review"
        ]
    ):

        if _contains_any(
            combined,
            [
                "meta-analysis",
                "meta analysis"
            ]
        ):

            _score_design(
                scores,
                "Systematic Review and Meta-analysis",
                100,
                "The research description explicitly indicates meta-analysis."
            )

        else:

            _score_design(
                scores,
                "Systematic Review",
                100,
                "The research description indicates a systematic review."
            )

    # ========================================================
    # 2. Randomized Controlled Trial
    # ========================================================

    if _contains_any(
        combined,
        [
            "randomized",
            "randomised",
            "random allocation",
            "random assignment",
            "randomly assigned",
            "randomized controlled trial",
            "rct"
        ]
    ):

        _score_design(
            scores,
            "Randomized Controlled Trial",
            100,
            "Random allocation is indicated."
        )

    # ========================================================
    # 3. Clinical Trial
    # ========================================================

    elif (
        intervention_text
        and
        _contains_any(
            combined,
            [
                "clinical trial",
                "trial",
                "treatment",
                "therapy",
                "therapeutic"
            ]
        )
    ):

        _score_design(
            scores,
            "Clinical Trial",
            70,
            "An intervention or treatment is being evaluated."
        )

    # ========================================================
    # 4. Diagnostic Accuracy
    # ========================================================

    if _contains_any(
        combined,
        [
            "diagnostic accuracy",
            "diagnostic test",
            "sensitivity",
            "specificity",
            "positive predictive value",
            "negative predictive value",
            "receiver operating characteristic",
            "roc curve",
            "auc"
        ]
    ):

        _score_design(
            scores,
            "Diagnostic Accuracy Study",
            90,
            "The study evaluates diagnostic test performance."
        )

    # ========================================================
    # 5. Case-Control
    # ========================================================

    if _contains_any(
        combined,
        [
            "case-control",
            "case control",
            "cases and controls",
            "cases versus controls"
        ]
    ):

        _score_design(
            scores,
            "Case-Control Study",
            100,
            "The study explicitly describes a case-control design."
        )

    # ========================================================
    # 6. Cross-sectional
    # ========================================================

    if _contains_any(
        combined,
        [
            "cross-sectional",
            "cross sectional",
            "prevalence survey",
            "prevalence study",
            "survey study"
        ]
    ):

        _score_design(
            scores,
            "Cross-Sectional Study",
            90,
            "The study has cross-sectional characteristics."
        )

    # ========================================================
    # 7. Prognostic / Survival
    # ========================================================

    survival_signal = _contains_any(
        combined,
        [
            "survival",
            "overall survival",
            "progression-free survival",
            "disease-free survival",
            "mortality",
            "time to event",
            "time-to-event",
            "kaplan-meier",
            "cox regression",
            "cox proportional hazards"
        ]
    )

    prognostic_signal = _contains_any(
        combined,
        [
            "prognostic",
            "prognostic factors",
            "predictors of survival",
            "predictors of mortality",
            "survival predictors"
        ]
    )

    if survival_signal or prognostic_signal:

        _score_design(
            scores,
            "Prognostic Study",
            85,
            "The research objective focuses on survival, mortality, or prognostic factors."
        )

    # ========================================================
    # 8. Cohort
    # ========================================================

    cohort_signal = _contains_any(
        combined,
        [
            "cohort",
            "follow-up",
            "follow up",
            "followup",
            "longitudinal",
            "prospective",
            "retrospective cohort"
        ]
    )

    if cohort_signal:

        if _contains_any(
            combined,
            [
                "prospective",
                "follow participants forward",
                "future follow-up"
            ]
        ):

            _score_design(
                scores,
                "Prospective Cohort Study",
                90,
                "The study indicates prospective follow-up."
            )

        else:

            _score_design(
                scores,
                "Retrospective Cohort Study",
                85,
                "The study indicates retrospective cohort characteristics."
            )

    # ========================================================
    # 9. Retrospective Observational
    # ========================================================

    retrospective_signal = _contains_any(
        combined,
        [
            "retrospective",
            "medical records",
            "hospital records",
            "registry",
            "registry database",
            "electronic health records",
            "ehr",
            "chart review",
            "record review",
            "retrospective data extraction"
        ]
    )

    observational_signal = _contains_any(
        combined,
        [
            "observational",
            "descriptive",
            "epidemiological",
            "epidemiology",
            "incidence",
            "prevalence",
            "distribution",
            "patterns",
            "trends"
        ]
    )

    if retrospective_signal and observational_signal:

        _score_design(
            scores,
            "Retrospective Observational Study",
            90,
            "The study uses retrospective records/data without a clear intervention."
        )

    elif retrospective_signal and not intervention_text:

        _score_design(
            scores,
            "Retrospective Observational Study",
            70,
            "Retrospective data collection is indicated and no intervention is specified."
        )

    # ========================================================
    # 10. Incidence / Epidemiological Study
    # ========================================================

    incidence_signal = _contains_any(
        combined,
        [
            "incidence",
            "incidence trends",
            "cancer incidence",
            "annual incidence",
            "new cases",
            "newly diagnosed cases",
            "disease burden",
            "epidemiological trends"
        ]
    )

    if incidence_signal:

        _score_design(
            scores,
            "Descriptive Epidemiological Study",
            80,
            "The research objective focuses on incidence, distribution, or epidemiological trends."
        )

    # ========================================================
    # 11. Ecological
    # ========================================================

    if _contains_any(
        combined,
        [
            "ecological",
            "population-level",
            "population level",
            "country-level",
            "country level",
            "regional-level",
            "regional level"
        ]
    ):

        _score_design(
            scores,
            "Ecological Study",
            80,
            "The unit of analysis appears to be a population or geographic group."
        )

    # ========================================================
    # 12. Default
    # ========================================================

    if not scores:

        _score_design(
            scores,
            "Retrospective Observational Study",
            40,
            "Insufficient information was provided; a conservative observational design is recommended."
        )

    # ========================================================
    # Special Rule:
    # Incidence retrospective record study
    # should NOT automatically become cohort.
    # ========================================================

    if (
        incidence_signal
        and retrospective_signal
        and not intervention_text
        and not _contains_any(
            combined,
            [
                "follow-up",
                "follow up",
                "time-to-event",
                "time to event",
                "survival",
                "mortality"
            ]
        )
    ):

        scores["Retrospective Observational Study"] = {
            "score": max(
                scores.get(
                    "Retrospective Observational Study",
                    {}
                ).get(
                    "score",
                    0
                ),
                100
            ),
            "reasons": [
                "Incidence/trend research based on retrospective records is better classified as retrospective observational rather than cohort when there is no follow-up outcome."
            ]
        }

    # ========================================================
    # Determine Winner
    # ========================================================

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    )

    best_design = ranked[0][0]
    best_score = ranked[0][1]["score"]
    reasons = ranked[0][1]["reasons"]

    # ========================================================
    # Confidence
    # ========================================================

    if best_score >= 100:
        confidence = 95

    elif best_score >= 90:
        confidence = 90

    elif best_score >= 80:
        confidence = 85

    elif best_score >= 70:
        confidence = 75

    else:
        confidence = 60

    # ========================================================
    # Alternatives
    # ========================================================

    alternatives = []

    for design, data in ranked[1:4]:

        if data["score"] <= 0:
            continue

        alternatives.append({
            "design": design,
            "score": data["score"],
            "reasons": data["reasons"]
        })

    # ========================================================
    # Warnings
    # ========================================================

    warnings = []

    if not goal:
        warnings.append(
            "Research goal was not provided."
        )

    if not source:
        warnings.append(
            "Data source was not provided."
        )

    if not method:
        warnings.append(
            "Collection method was not provided."
        )

    if (
        best_design in [
            "Retrospective Cohort Study",
            "Prospective Cohort Study"
        ]
        and not outcome_text
    ):
        warnings.append(
            "A cohort study normally requires a clearly defined outcome and follow-up structure."
        )

    if (
        best_design == "Prognostic Study"
        and not outcome_text
    ):
        warnings.append(
            "A prognostic study should specify the prognostic outcome."
        )

    if (
        best_design == "Clinical Trial"
        and not intervention_text
    ):
        warnings.append(
            "A clinical trial normally requires a clearly defined intervention."
        )

    # ========================================================
    # Category
    # ========================================================

    if best_design in [
        "Randomized Controlled Trial",
        "Clinical Trial"
    ]:
        category = "Interventional"

    elif best_design in [
        "Retrospective Cohort Study",
        "Prospective Cohort Study",
        "Cross-Sectional Study",
        "Case-Control Study",
        "Retrospective Observational Study",
        "Ecological Study",
        "Descriptive Epidemiological Study",
        "Prognostic Study",
        "Diagnostic Accuracy Study"
    ]:
        category = "Observational"

    elif best_design in [
        "Systematic Review",
        "Systematic Review and Meta-analysis"
    ]:
        category = "Evidence Synthesis"

    else:
        category = "Other"

    return {
        "recommended_design": best_design,
        "design_category": category,
        "confidence": confidence,
        "score": best_score,
        "reasons": reasons,
        "alternatives": alternatives,
        "warnings": warnings,
    }


# ============================================================
# Convenience Function
# ============================================================

def recommend_study_design(
    research_context=None
):

    context = research_context or {}

    return classify_study_design(
        research_goal=context.get(
            "research_goal",
            ""
        ),

        data_source=context.get(
            "data_source",
            ""
        ),

        collection_method=context.get(
            "collection_method",
            ""
        ),

        population=context.get(
            "population",
            ""
        ),

        intervention=context.get(
            "intervention",
            ""
        ),

        comparison=context.get(
            "comparison",
            ""
        ),

        outcome=context.get(
            "outcome",
            ""
        ),

        study_period=context.get(
            "study_period",
            context.get(
                "period",
                ""
            )
        ),

        sampling_method=context.get(
            "sampling_method",
            ""
        ),

        research_question=context.get(
            "research_question",
            ""
        ),

        topic=context.get(
            "disease",
            context.get(
                "topic",
                ""
            )
        )
    )
