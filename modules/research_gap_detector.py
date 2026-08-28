from collections import Counter
import re


def detect_research_gaps(
    papers,
    research_context=None
):

    keyword_counter = Counter()
    publication_types = Counter()
    journals = Counter()

    total_papers = len(papers)

    research_context = (
        research_context or {}
    )
    research_goal = str(
        research_context.get(
            "research_goal",
            ""
        )
    ).lower()
    study_design = str(
        research_context.get(
            "recommended_design",
            research_context.get(
                "study_design",
                ""
            )
        )
    ).lower()

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
    # Dynamic Evidence Level Analysis
    # =========================

    level1 = levels.get(
        "Level 1",
        0
    )

    level2 = levels.get(
        "Level 2",
        0
    )


    if (
        "systematic review" in study_design
        or
        "meta-analysis" in study_design
    ):
        if level1 == 0:
            gaps.append(
                "No high-level review evidence identified."
            )
    elif (
        "trial" in study_design
        or
        "randomized" in study_design
    ):
        if level2 < 3:
            gaps.append(
                "Limited clinical trial evidence."
            )
    elif (
        "cohort" in study_design
    ):
        if level2 == 0 and level1 == 0:
            gaps.append(
                "Limited longitudinal evidence."
            )
    elif (
        "diagnostic" in study_design
    ):
        gaps.append(
            "Need further validation of diagnostic performance across populations."
        )
    elif (
        "prognostic" in study_design
    ):
        gaps.append(
            "Need external validation of prognostic findings."
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



    # =========================
    # Recent Evidence Analysis
    # =========================

    years = []
    for paper in papers:
        year = paper.get(
            "year"
        )
        try:
            years.append(
                int(year)
            )
        except Exception:
            pass
    recent_ratio = 0
    if years:
        recent_count = len(
            [
                y
                for y in years
                if y >= 2020
            ]
        )
        recent_ratio = round(
            recent_count
            /
            len(years)
            *
            100,
            1
        )
        if recent_ratio < 30:
            gaps.append(
                "Limited recent evidence available."
            )



    # =========================
    # Target Population Analysis
    # =========================

    population_keywords = [
        "children",
        "pediatric",
        "elderly",
        "women",
        "pregnant"
    ]
    population_hits = 0
    for paper in papers:
        title = paper.get(
            "title",
            ""
        ).lower()
        if any(
            x in title
            for x in population_keywords
        ):
            population_hits += 1
    if (
        total_papers > 0
        and
        population_hits < 3
    ):
        gaps.append(
            "Limited evidence in special populations."
        )



    # =========================
    # Gap Score Calculation
    # =========================

    gap_score = max(
        0,
        100 - len(gaps) * 10
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
        gaps,


        "gap_score":
        gap_score,


        "recent_evidence_ratio":
        recent_ratio,


        "gap_count":
        len(gaps)

    }
