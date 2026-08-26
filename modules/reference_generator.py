def generate_references(
    literature,
    style="Vancouver"
):

    references = []

    for i, paper in enumerate(
        literature,
        start=1
    ):

        authors = paper.get(
            "authors",
            "Unknown Authors"
        )

        title = paper.get(
            "title",
            "Untitled"
        )

        journal = paper.get(
            "journal",
            "Unknown Journal"
        )

        year = paper.get(
            "year",
            ""
        )

        doi = paper.get(
            "doi",
            ""
        )

        pmid = paper.get(
            "pmid",
            ""
        )

        if style == "Vancouver":

            reference = (
                f"[{i}] "
                f"{authors}. "
                f"{title}. "
                f"{journal}. "
                f"{year}."
            )

            if doi:

                reference += (
                    f" DOI: {doi}."
                )

            elif pmid:

                reference += (
                    f" PMID: {pmid}."
                )

        else:

            reference = (
                f"[{i}] "
                f"{authors}. "
                f"{title}. "
                f"{journal}. "
                f"{year}."
            )

            if doi:

                reference += (
                    f" DOI: {doi}."
                )

            elif pmid:

                reference += (
                    f" PMID: {pmid}."
                )

        references.append(
            reference
        )

    return "\n".join(
        references
    )
