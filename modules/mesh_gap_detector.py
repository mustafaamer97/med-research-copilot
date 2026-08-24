from collections import Counter


def detect_mesh_gaps(papers):

    mesh_counter = Counter()

    publication_counter = Counter()

    country_counter = Counter()

    for paper in papers:

        # MeSH Terms

        mesh_terms = paper.get(
            "mesh_terms",
            ""
        )

        if mesh_terms:

            for term in mesh_terms.split(","):

                term = term.strip()

                if term:

                    mesh_counter.update(
                        [term]
                    )

        # Study Type

        publication_type = paper.get(
            "publication_type",
            ""
        )

        if publication_type:

            publication_counter.update(
                [publication_type]
            )

        # Country

        country = paper.get(
            "country",
            ""
        )

        if country:

            country_counter.update(
                [country]
            )

    return {

        "top_mesh_terms":
        mesh_counter.most_common(30),

        "top_study_types":
        publication_counter.most_common(15),

        "top_countries":
        country_counter.most_common(15)

    }
