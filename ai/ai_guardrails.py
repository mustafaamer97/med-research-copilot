FORBIDDEN_TERMS = [

    # References
    "invent doi",
    "invent pmid",
    "fake reference",
    "fabricate citation",
    "fabricate reference",

    # Statistics
    "invent statistical result",
    "fake p-value",
    "fake sample size",

    # Research misconduct
    "make up data",
    "fabricate data",
    "generate fake dataset",
    "create fake results",

    # Publications
    "invent study",
    "invent clinical trial",
    "fake publication"
]


def validate_prompt(prompt):

    text = prompt.lower()

    for term in FORBIDDEN_TERMS:

        if term in text:
            return False

    return True
