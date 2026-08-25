import requests

from modules.evidence_classifier import (
    classify_evidence_level
)


def search_openalex(
    query,
    max_results=20
):

    url = (
        "https://api.openalex.org/works"
    )

    params = {
        "search": query,
        "per-page": max_results
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        data = response.json()

    except Exception as e:

        print(
            f"OpenAlex Error: {e}"
        )

        return []

    results = data.get(
        "results",
        []
    )

    papers = []

    for item in results:

        title = item.get(
            "title",
            ""
        )

        year = item.get(
            "publication_year",
            ""
        )

        doi = (
            item.get("doi", "")
            .replace(
                "https://doi.org/",
                ""
            )
        )

        citation_count = item.get(
            "cited_by_count",
            0
        )

        abstract = ""

        publication_type = (
            item.get(
                "type",
                ""
            )
        )

        evidence_level = (
            classify_evidence_level(
                publication_type
            )
        )

        papers.append(
            {
                "pmid": "",

                "title": title,

                "authors": "",

                "journal": "",

                "year": str(year),

                "doi": doi,

                "url": item.get(
                    "id",
                    ""
                ),

                "publication_type":
                publication_type,

                "evidence_level":
                evidence_level,

                "abstract":
                abstract,

                "citation_count":
                citation_count,

                "source":
                "OpenAlex"
            }
        )

    return papers
