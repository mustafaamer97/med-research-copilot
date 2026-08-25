from collections import Counter


def recommend_journals(
    literature,
    medical_field=""
):

    journals = []

    for paper in literature:

        journal = paper.get(
            "journal",
            ""
        )

        if journal:

            journals.append(
                journal
            )

    counts = Counter(
        journals
    )

    recommendations = []

    for journal, count in counts.most_common(10):

        recommendations.append(
            {
                "journal": journal,
                "supporting_papers": count
            }
        )

    return recommendations
