def calculate_evidence_score(paper):

    score = 0


    # =========================
    # Evidence Level Priority
    # =========================

    level = paper.get(
        "evidence_level",
        "Unknown"
    )

    publication_type = (
        paper.get(
            "publication_type",
            ""
        ).lower()
    )

    if level == "Unknown":

        if (
            "meta-analysis" in publication_type
            or
            "systematic review" in publication_type
        ):
            level = "Level 1"

        elif (
            "randomized" in publication_type
            or
            "clinical trial" in publication_type
        ):
            level = "Level 2"

        elif (
            "cohort" in publication_type
            or
            "case-control" in publication_type
        ):
            level = "Level 3"

        elif (
            "cross-sectional" in publication_type
        ):
            level = "Level 4"

    paper["evidence_level"] = level


    evidence_scores = {

        "Level 1": 100,

        "Level 2": 90,

        "Level 3": 75,

        "Level 4": 60,

        "Level 5": 40,

        "Unknown": 20

    }


    score += evidence_scores.get(
        level,
        20
    )


    # =========================
    # Publication Type Bonus
    # =========================

    publication_type = (
        paper.get(
            "publication_type",
            ""
        )
        .lower()
    )


    if "meta-analysis" in publication_type:

        score += 20


    elif "systematic review" in publication_type:

        score += 15


    elif (
        "randomized" in publication_type
        or
        "clinical trial" in publication_type
    ):

        score += 10



    # =========================
    # Recent Evidence Bonus
    # =========================

    try:

        year = int(
            paper.get(
                "year",
                0
            )
        )

        if year >= 2024:

            score += 15

        elif year >= 2020:

            score += 10

        elif year >= 2015:

            score += 5


    except:

        pass



    # =========================
    # Citation Impact
    # =========================

    try:

        citations = int(
            paper.get(
                "citation_count",
                0
            )
        )


        if citations >= 200:

            score += 15


        elif citations >= 50:

            score += 10


        elif citations >= 10:

            score += 5


    except:

        pass



    return score



# ==================================
# Rank Evidence
# ==================================

def rank_evidence(papers):


    for paper in papers:

        paper[
            "evidence_score"
        ] = calculate_evidence_score(
            paper
        )


    papers.sort(
        key=lambda x:
        x.get(
            "evidence_score",
            0
        ),
        reverse=True
    )


    return papers
