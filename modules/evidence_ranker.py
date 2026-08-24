def calculate_evidence_score(paper):

    publication_type = (
        paper.get("publication_type", "")
        .lower()
    )

    score = 0

    # أعلى مستوى من الأدلة

    if "meta-analysis" in publication_type:
        score += 100

    elif "systematic review" in publication_type:
        score += 95

    elif (
        "randomized controlled trial" in publication_type
        or "randomized" in publication_type
        or "clinical trial" in publication_type
    ):
        score += 90

    elif "cohort" in publication_type:
        score += 70

    elif "case-control" in publication_type:
        score += 60

    elif "cross-sectional" in publication_type:
        score += 50

    elif "case series" in publication_type:
        score += 30

    elif "case report" in publication_type:
        score += 20

    # مكافأة للمقالات الحديثة

    try:

        year = int(
            paper.get("year", 0)
        )

        if year >= 2023:
            score += 10

        elif year >= 2020:
            score += 5

    except:
        pass

    return score


def rank_evidence(papers):

    ranked_papers = []

    for paper in papers:

        paper["evidence_score"] = (
            calculate_evidence_score(
                paper
            )
        )

        ranked_papers.append(paper)

    ranked_papers.sort(
        key=lambda x: x["evidence_score"],
        reverse=True
    )

    return ranked_papers
