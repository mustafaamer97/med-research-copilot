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



def normalize_paper(
    paper,
    source
):

    return {

        "title":
        paper.get(
            "title",
            ""
        ),

        "authors":
        paper.get(
            "authors",
            ""
        ),

        "year":
        paper.get(
            "year",
            ""
        ),

        "doi":
        paper.get(
            "doi",
            ""
        ),

        "pmid":
        paper.get(
            "pmid",
            ""
        ),

        "abstract":
        paper.get(
            "abstract",
            ""
        ),

        "url":
        paper.get(
            "url",
            ""
        ),

        "publication_type":
        paper.get(
            "publication_type",
            ""
        ),

        "evidence_level":
        paper.get(
            "evidence_level",
            "Unknown"
        ),

        "source":
        source,

        "citation_count":
        paper.get(
            "citation_count",
            0
        )

    }



def search_all_sources(
    query,
    max_results=20
):

    papers = []


    # =========================
    # PubMed
    # =========================

    try:

        pubmed = get_recent_evidence(
            query
        )

        for paper in pubmed:

            papers.append(
                normalize_paper(
                    paper,
                    "PubMed"
                )
            )


    except Exception as e:

        print(
            f"PubMed Error: {e}"
        )



    # =========================
    # Europe PMC
    # =========================

    try:

        epmc = search_europe_pmc(
            query,
            max_results
        )

        for paper in epmc:

            papers.append(
                normalize_paper(
                    paper,
                    "Europe PMC"
                )
            )


    except Exception as e:

        print(
            f"Europe PMC Error: {e}"
        )



    # =========================
    # OpenAlex
    # =========================

    try:

        openalex = search_openalex(
            query,
            max_results
        )

        for paper in openalex:

            papers.append(
                normalize_paper(
                    paper,
                    "OpenAlex"
                )
            )


    except Exception as e:

        print(
            f"OpenAlex Error: {e}"
        )



    # =========================
    # Deduplicate
    # =========================

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


    # =========================
    # Evidence Ranking
    # =========================

    papers = rank_evidence(
        papers
    )


    return papers[:max_results]
