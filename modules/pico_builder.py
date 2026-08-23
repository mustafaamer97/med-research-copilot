def build_pico(
    population,
    intervention,
    comparison,
    outcome
):

    question = (
        f"In {population}, "
        f"does {intervention} "
        f"compared with {comparison} "
        f"improve {outcome}?"
    )


    keywords = (
        f"{population} AND "
        f"{intervention} AND "
        f"{comparison} AND "
        f"{outcome}"
    )


    return {
        "question": question,
        "keywords": keywords
    }
