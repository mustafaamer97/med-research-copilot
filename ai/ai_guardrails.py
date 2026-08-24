FORBIDDEN_TERMS = [
    "invent doi",
    "invent pmid",
    "fake reference",
    "fabricate citation",
    "invent statistical result",
    "fake p-value",
    "fake sample size"
]


def validate_prompt(prompt):

    text = prompt.lower()

    for term in FORBIDDEN_TERMS:

        if term in text:

            return False

    return True
