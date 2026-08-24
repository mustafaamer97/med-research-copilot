from collections import Counter
import re


def detect_research_gaps(papers):

    keyword_counter = Counter()

    publication_types = Counter()

    journals = Counter()

    total_papers = len(papers)

    for paper in papers:

        # الكلمات من العنوان

        title = paper.get(
            "title",
            ""
        ).lower()

        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            title
        )

        keyword_counter.update(words)

        # نوع الدراسة

        publication_type = paper.get(
            "publication_type",
            ""
        )

        if publication_type:

            publication_types.update(
                [publication_type]
            )

        # المجلة

        journal = paper.get(
            "journal",
            ""
        )

        if journal:

            journals.update(
                [journal]
            )

    return {
        "total_papers": total_papers,
        "top_keywords": keyword_counter.most_common(20),
        "study_types": publication_types.most_common(10),
        "top_journals": journals.most_common(10)
    }
