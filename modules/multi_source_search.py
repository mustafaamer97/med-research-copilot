from modules.evidence_search import (
    get_recent_evidence
)

from modules.evidence_ranker import (
    rank_evidence
)


def search_all_sources(query):

    papers = []

    try:

        pubmed_papers = get_recent_evidence(
            query
        )

        papers.extend(
            pubmed_papers
        )

    except Exception as e:

        print(
            f"PubMed error: {e}"
        )

    # Europe PMC
    # سيتم إضافته هنا لاحقاً

    # OpenAlex
    # سيتم إضافته هنا لاحقاً

    # إزالة التكرار

    unique = {}

    for paper in papers:

        key = (
            paper.get("doi")
            or paper.get("pmid")
            or paper.get("title")
        )

        if key:
            unique[key] = paper

    papers = list(
        unique.values()
    )

    papers = rank_evidence(
        papers
    )

    return papers
