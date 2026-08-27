import requests

from modules.evidence_classifier import (
    classify_evidence_level
)



def extract_abstract(item):

    inverted = item.get(
        "abstract_inverted_index",
        {}
    )


    if not inverted:

        return ""


    words = []


    for word, positions in inverted.items():

        for pos in positions:

            words.append(
                (
                    pos,
                    word
                )
            )


    words.sort(
        key=lambda x:x[0]
    )


    return " ".join(
        [
            w[1]
            for w in words
        ]
    )





def search_openalex(
    query,
    max_results=20
):

    url = (
        "https://api.openalex.org/works"
    )


    params = {

        "search":
        query,

        "per-page":
        max_results
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



    papers = []


    for item in data.get(
        "results",
        []
    ):


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


        doi = item.get(
            "doi",
            ""
        )


        if doi:

            doi = doi.replace(
                "https://doi.org/",
                ""
            )



        papers.append(

            {

            "pmid":
            "",


            "title":
            item.get(
                "title",
                ""
            ),


            "authors":
            "",


            "journal":
            "",


            "year":
            str(
                item.get(
                    "publication_year",
                    ""
                )
            ),


            "doi":
            doi,


            "url":
            item.get(
                "id",
                ""
            ),


            "publication_type":
            publication_type,


            "evidence_level":
            evidence_level,


            "abstract":
            extract_abstract(
                item
            ),


            "citation_count":
            item.get(
                "cited_by_count",
                0
            ),


            "source":
            "OpenAlex"

            }

        )


    return papers
