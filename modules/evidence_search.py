from modules.pubmed import search_pubmed


PRIORITY_FILTERS = [
    "systematic review",
    "meta-analysis",
    "randomized controlled trial",
    "clinical trial",
    "cohort study",
    "observational study"
]


def get_recent_evidence(topic):

    all_papers = []

    for study_type in PRIORITY_FILTERS:

        query = f"{topic} AND {study_type}"

        try:

            papers = search_pubmed(
                query,
                max_results=10
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

    return papers[:20]
