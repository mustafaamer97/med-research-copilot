from collections import Counter
import re


def detect_research_gaps(papers):

    keyword_counter = Counter()
    publication_types = Counter()
    journals = Counter()

    total_papers = len(papers)

    evidence_scores = []

    levels = Counter()


    for paper in papers:

        title = paper.get(
            "title",
            ""
        ).lower()


        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            title
        )

        keyword_counter.update(
            words
        )


        publication_type = (
            paper.get(
                "publication_type",
                ""
            )
            or
            paper.get(
                "type",
                ""
            )
        )


        if publication_type:

            publication_types.update(
                [publication_type]
            )


        journal = paper.get(
            "journal",
            ""
        )

        if journal:

            journals.update(
                [journal]
            )


        level = paper.get(
            "evidence_level",
            "Unknown"
        )

        levels.update(
            [level]
        )


        score = paper.get(
            "evidence_score",
            0
        )

        if score:

            evidence_scores.append(
                score
            )



    gaps = []


    # =========================
    # Evidence Level Analysis
    # =========================

    level1 = levels.get(
        "Level 1",
        0
    )

    level2 = levels.get(
        "Level 2",
        0
    )


    if level1 == 0:

        gaps.append(
            "No high-level evidence identified (systematic reviews/meta-analyses)."
        )


    if level2 < 3:

        gaps.append(
            "Limited randomized clinical trial evidence."
        )



    # =========================
    # Evidence Quantity
    # =========================

    if total_papers < 10:

        gaps.append(
            "Limited number of available studies."
        )


    # =========================
    # Evidence Diversity
    # =========================

    if len(journals) < 3:

        gaps.append(
            "Evidence comes from a limited number of journals."
        )



    # =========================
    # Study Type Diversity
    # =========================

    if len(publication_types) < 3:

        gaps.append(
            "Limited diversity of study designs."
        )



    # =========================
    # Evidence Strength
    # =========================

    if evidence_scores:

        average_score = round(
            sum(evidence_scores)
            /
            len(evidence_scores),
            2
        )

    else:

        average_score = 0



    if average_score < 50:

        gaps.append(
            "Overall evidence strength is relatively low."
        )



    return {


        "total_papers":
        total_papers,


        "top_keywords":
        keyword_counter.most_common(20),


        "study_types":
        publication_types.most_common(10),


        "top_journals":
        journals.most_common(10),


        "evidence_distribution":
        dict(levels),


        "average_evidence_score":
        average_score,


        "research_gaps":
        gaps

    }
