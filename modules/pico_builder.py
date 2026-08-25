import re


def extract_search_terms(text):

    if not text:
        return []

    text = text.lower()

    stop_words = {
        "with",
        "without",
        "compared",
        "comparison",
        "versus",
        "vs",
        "effect",
        "effects",
        "improve",
        "improves",
        "improved",
        "reduction",
        "increase",
        "decrease",
        "adults",
        "adult",
        "children",
        "child",
        "patients",
        "patient",
        "population",
        "group",
        "study",
        "trial",
        "outcome",
        "outcomes",
        "the",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "to"
    }

    words = re.findall(
        r"[a-zA-Z0-9\-]+",
        text
    )

    keywords = []

    for word in words:

        if len(word) < 3:
            continue

        if word in stop_words:
            continue

        keywords.append(word)

    return list(
        dict.fromkeys(keywords)
    )


def build_pico(
    population,
    intervention,
    comparison,
    outcome
):

    missing = []

    if not population:
        missing.append("Population")

    if not intervention:
        missing.append("Intervention")

    if not outcome:
        missing.append("Outcome")

    if missing:

        return {
            "error":
            f"Missing: {', '.join(missing)}"
        }

    question = (
        f"In {population}, "
        f"does {intervention} "
        f"compared with {comparison} "
        f"improve {outcome}?"
    )

    search_terms = []

    search_terms.extend(
        extract_search_terms(
            population
        )
    )

    search_terms.extend(
        extract_search_terms(
            intervention
        )
    )

    search_terms.extend(
        extract_search_terms(
            outcome
        )
    )

    search_terms = list(
        dict.fromkeys(search_terms)
    )

    keywords = " AND ".join(
        search_terms[:8]
    )

    return {
        "question": question,
        "keywords": keywords
    }
