from modules.pubmed import search_pubmed


def build_evidence_filters(research_context):
    goal = str(
        research_context.get(
            "research_goal",
            ""
        )
    ).lower()
    design = str(
        research_context.get(
            "recommended_design",
            research_context.get(
                "study_design",
                ""
            )
        )
    ).lower()
    if "systematic review" in design:
        return [
            "systematic review",
            "meta-analysis"
        ]
    if "meta-analysis" in design:
        return [
            "meta-analysis",
            "systematic review"
        ]
    if "diagnostic" in design:
        return [
            "diagnostic accuracy",
            "sensitivity",
            "specificity",
            "roc"
        ]
    if "prognostic" in design:
        return [
            "prognostic",
            "survival",
            "mortality",
            "cox regression"
        ]
    if "prediction" in design:
        return [
            "prediction model",
            "risk model",
            "machine learning"
        ]
    if "case-control" in design:
        return [
            "case-control study",
            "risk factors"
        ]
    if "cross-sectional" in design:
        return [
            "cross-sectional study",
            "prevalence"
        ]
    if "cohort" in design:
        return [
            "cohort study",
            "follow-up"
        ]
    if goal.lower() == "survival analysis":
        return [
            "survival",
            "kaplan-meier",
            "cox regression"
        ]
    return [
        "observational study",
        "cohort study"
    ]


def get_recent_evidence(research_context):

    topic = research_context.get(
        "disease",
        ""
    )
    population = research_context.get(
        "population",
        ""
    )
    outcome = research_context.get(
        "outcome",
        ""
    )
    filters = build_evidence_filters(
        research_context
    )
    all_papers = []

    for study_type in filters:

        query_parts = [
            topic,
            study_type
        ]
        if population:
            query_parts.append(population)
        if outcome:
            query_parts.append(outcome)
        query = " AND ".join(
            [
                x
                for x in query_parts
                if x
            ]
        )

        try:

            papers = search_pubmed(
                query,
                max_results=20
            )

            all_papers.extend(papers)

        except Exception as e:

            print(
                f"Evidence search error ({study_type}): {e}"
            )

    # إزالة التكرار بواسطة PMID

    unique_papers = {}

    for paper in all_papers:

        pmid = paper.get("pmid")

        if pmid:

            unique_papers[pmid] = paper

    papers = list(
        unique_papers.values()
    )

    # ترتيب حسب مستوى الدليل

    ranking = {
        "Level 1": 1,
        "Level 2": 2,
        "Level 3": 3,
        "Level 4": 4,
        "Level 5": 5,
        "Unknown": 99
    }

    papers.sort(
        key=lambda paper: ranking.get(
            paper.get(
                "evidence_level",
                "Unknown"
            ),
            99
        )
    )

    return papers[:40]
