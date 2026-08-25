from collections import Counter
import re


def detect_research_gaps(papers):

    keyword_counter = Counter()
    publication_types = Counter()
    journals = Counter()

    total_papers = len(papers)

    for paper in papers:

        title = paper.get(
            "title",
            ""
        ).lower()

        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            title
        )

        keyword_counter.update(words)

        publication_type = paper.get(
            "publication_type",
            ""
        )

        if publication_type:

            publication_types.update(
                [publication_type]
            )

        journal = paper.get(
            "journal",
            ""
        )

        if journal:

            journals.update(
                [journal]
            )

    gaps = []

    level1_count = len([
        p for p in papers
        if p.get("evidence_level")
        == "Level 1"
    ])

    if level1_count == 0:

        gaps.append(
            "No systematic reviews or meta-analyses identified."
        )

    trial_count = len([
        p for p in papers
        if "trial" in str(
            p.get(
                "publication_type",
                ""
            )
        ).lower()
    ])

    if trial_count < 3:

        gaps.append(
            "Limited randomized or clinical trial evidence."
        )

    if total_papers < 10:

        gaps.append(
            "Small evidence base available."
        )

    if len(journals) < 3:

        gaps.append(
            "Evidence concentrated in few journals."
        )

    return {
        "total_papers": total_papers,
        "top_keywords": keyword_counter.most_common(20),
        "study_types": publication_types.most_common(10),
        "top_journals": journals.most_common(10),
        "research_gaps": gaps
    }
