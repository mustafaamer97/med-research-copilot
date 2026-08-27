import requests

from modules.evidence_classifier import (
    classify_evidence_level
)


def search_europe_pmc(
    query,
    max_results=20
):

    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    )

    params = {
        "query": query,
        "format": "json",
        "pageSize": max_results,
        "resultType": "core"
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
            f"Europe PMC Error: {e}"
        )

        return []

    results = data.get(
        "resultList",
        {}
    ).get(
        "result",
        []
    )

    papers = []

    for item in results:

        publication_type = (
            item.get(
                "pubType",
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
                "pmid": item.get(
                    "pmid",
                    ""
                ),

                "title": item.get(
                    "title",
                    ""
                ),

                "authors": item.get(
                    "authorString",
                    ""
                ),

                "journal": item.get(
                    "journalTitle",
                    ""
                ),

                "year": str(
                    item.get(
                        "pubYear",
                        ""
                    )
                ),

                "publication_date": item.get(
                    "firstPublicationDate",
                    ""
                ),

                "doi": item.get(
                    "doi",
                    ""
                ),

                "url":
                f"https://europepmc.org/article/{item.get('source','')}/{item.get('id','')}",

                "publication_type":
                publication_type,

                "evidence_level":
                evidence_level,

                "abstract":
                item.get(
                    "abstractText",
                    ""
                ),

                "citation_count":
                item.get(
                    "citedByCount",
                    0
                ),

                "is_open_access":
                item.get(
                    "isOpenAccess",
                    "N"
                ) == "Y",

                "source":
                "Europe PMC"
            }
        )

    return papers
