import re


def insert_vancouver_citations(
    manuscript,
    literature
):

    if not manuscript:
        return manuscript

    if not literature:
        return manuscript

    for index, paper in enumerate(
        literature,
        start=1
    ):

        title = paper.get(
            "title",
            ""
        )

        if not title:
            continue

        words = title.split()

        if not words:
            continue

        keyword = words[0]

        pattern = (
            rf"\b{re.escape(keyword)}\b"
        )

        replacement = (
            f"{keyword} [{index}]"
        )

        manuscript = re.sub(
            pattern,
            replacement,
            manuscript,
            count=1
        )

    return manuscript
