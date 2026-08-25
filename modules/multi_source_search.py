from modules.evidence_search import (
    get_recent_evidence
)

from modules.evidence_ranker import (
    rank_evidence
)

from modules.europe_pmc import (
    search_europe_pmc
)

from modules.openalex import (
    search_openalex
)


def search_all_sources(query):

    papers = []

    # PubMed

    try:

        pubmed_papers = (
            get_recent_evidence(
                query
            )
        )

        papers.extend(
            pubmed_papers
        )

    except Exception as e:

        print(
            f"PubMed Error: {e}"
        )

    # Europe PMC

    try:

        epmc_papers = (
            search_europe_pmc(
                query,
                20
            )
        )

        papers.extend(
            epmc_papers
        )

    except Exception as e:

        print(
            f"Europe PMC Error: {e}"
        )

    # OpenAlex

    try:

        openalex_papers = (
            search_openalex(
                query,
                20
            )
        )

        papers.extend(
            openalex_papers
        )

    except Exception as e:

        print(
            f"OpenAlex Error: {e}"
        )

    # Deduplicate

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
