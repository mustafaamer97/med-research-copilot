import re

FORBIDDEN_PATTERNS = [

    # Fake references
    r"invent.*doi",
    r"invent.*pmid",
    r"fake.*reference",
    r"fabricate.*citation",
    r"fabricate.*reference",
    r"create.*fake.*reference",

    # Fake statistics
    r"invent.*statistical",
    r"fake.*p[\-\s]?value",
    r"fabricate.*result",
    r"create.*fake.*result",
    r"invent.*sample\s*size",

    # Research misconduct
    r"make\s*up.*data",
    r"fabricate.*data",
    r"generate.*fake.*dataset",
    r"create.*fake.*dataset",
    r"fake.*clinical.*trial",
    r"invent.*clinical.*trial",

    # Publications
    r"invent.*study",
    r"fake.*publication",
    r"fabricate.*paper",

    # Ethics violations
    r"bypass.*irb",
    r"skip.*ethics",
    r"fake.*consent",
    r"fabricate.*consent",

    # Fraudulent reporting
    r"change.*p[\-\s]?value",
    r"adjust.*result.*significant",
    r"make.*result.*significant",
]


def validate_prompt(prompt: str) -> bool:
    """
    Returns True if prompt is allowed.
    Returns False if prompt contains potentially
    fraudulent research instructions.
    """

    if not prompt:
        return True

    text = prompt.lower().strip()

    for pattern in FORBIDDEN_PATTERNS:

        if re.search(pattern, text):
            return False

    return True
