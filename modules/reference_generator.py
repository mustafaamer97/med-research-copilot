def generate_references(
    literature,
    style="Vancouver"
):

    references = []
    seen = set()

    for i, paper in enumerate(
        literature,
        start=1
    ):

        doi = str(
            paper.get("doi", "")
        ).strip()

        if doi:

            if doi in seen:
                continue

            seen.add(doi)

        authors = paper.get(
            "authors",
            []
        )

        if isinstance(
            authors,
            list
        ):

            if len(authors) > 6:

                authors = (
                    ", ".join(authors[:6])
                    + ", et al"
                )

            else:

                authors = ", ".join(authors)

        if not authors:
            authors = "Unknown Authors"

        title = (
            paper.get("title", "")
            or "Untitled"
        )

        journal = (
            paper.get("journal", "")
            or "Unknown Journal"
        )

        year = (
            paper.get("year", "")
            or ""
        )

        pmid = str(
            paper.get("pmid", "")
        ).strip()

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

        if pmid:

            reference += (
                f" PMID: {pmid}."
            )

        references.append(
            reference
        )

    return "\n".join(
        references
    )        references
    )
