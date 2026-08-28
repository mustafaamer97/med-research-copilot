def classify_evidence_level(publication_type):

    if not publication_type:
        return "Unknown"

    text = publication_type.lower()

    # ====================================
    # Level 1
    # ====================================

    if any(
        x in text
        for x in [
            "meta-analysis",
            "meta analysis",
            "systematic review",
            "network meta-analysis",
            "umbrella review"
        ]
    ):
        return "Level 1"

    # ====================================
    # Level 2
    # ====================================

    if any(
        x in text
        for x in [
            "randomized controlled trial",
            "randomized",
            "clinical trial",
            "controlled clinical trial",
            "pragmatic trial"
        ]
    ):
        return "Level 2"

    # ====================================
    # Level 3 (Cohort, Prospective, Retrospective, Diagnostic, Prognostic, Prediction)
    # ====================================

    if any(
        x in text
        for x in [
            "cohort",
            "prospective study",
            "retrospective study",
            "prognostic study",
            "diagnostic accuracy",
            "diagnostic study",
            "prediction model",
            "follow-up",
            "longitudinal"
        ]
    ):
        return "Level 3"

    # ====================================
    # Level 4 (Case-Control, Cross-Sectional, Observational)
    # ====================================

    if any(
        x in text
        for x in [
            "case-control",
            "case control",
            "cross-sectional",
            "cross sectional",
            "observational study",
            "observational"
        ]
    ):
        return "Level 4"

    # ====================================
    # Level 5
    # ====================================

    if any(
        x in text
        for x in [
            "case series",
            "case report"
        ]
    ):
        return "Level 5"

    return "Unknown"


# ====================================
# Evidence Score Assessment
# ====================================

def evidence_score(level):
    scores = {
        "Level 1": 100,
        "Level 2": 90,
        "Level 3": 75,
        "Level 4": 60,
        "Level 5": 40,
        "Unknown": 20
    }
    return scores.get(level, 20)
