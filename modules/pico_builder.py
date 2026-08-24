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

    keywords = (
        f"({population}) AND "
        f"({intervention}) AND "
        f"({comparison}) AND "
        f"({outcome})"
    )

    return {
        "question": question,
        "keywords": keywords
    }
