def classify_evidence_level(publication_type):

    if not publication_type:
        return "Unknown"

    publication_type = publication_type.lower()

    # Level 1
    if (
        "meta-analysis" in publication_type
        or "systematic review" in publication_type
    ):
        return "Level 1"

    # Level 2
    if (
        "randomized controlled trial" in publication_type
        or "randomized" in publication_type
        or "clinical trial" in publication_type
    ):
        return "Level 2"

    # Level 3
    if (
        "cohort" in publication_type
        or "prospective study" in publication_type
        or "retrospective study" in publication_type
    ):
        return "Level 3"

    # Level 4
    if (
        "case-control" in publication_type
        or "cross-sectional" in publication_type
        or "observational study" in publication_type
    ):
        return "Level 4"

    # Level 5
    if (
        "case series" in publication_type
        or "case report" in publication_type
    ):
        return "Level 5"

    return "Unknown"
