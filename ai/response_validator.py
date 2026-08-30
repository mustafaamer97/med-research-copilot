import re

FORBIDDEN_PATTERNS = [

    # Fake identifiers
    r"fake\s*doi",
    r"fake\s*pmid",
    r"invented\s*doi",
    r"invented\s*pmid",
    r"fabricated\s*doi",
    r"fabricated\s*pmid",

    # Fake references
    r"fabricated\s*reference",
    r"fake\s*reference",
    r"invented\s*reference",
    r"generated\s*reference",

    # Fake studies
    r"fabricated\s*study",
    r"invented\s*study",
    r"fake\s*clinical\s*trial",

    # Fake statistics
    r"fabricated\s*p[\-\s]?value",
    r"fake\s*p[\-\s]?value",
    r"invented\s*p[\-\s]?value",

    r"fabricated\s*sample\s*size",
    r"fake\s*sample\s*size",

    r"fabricated\s*confidence\s*interval",
    r"fabricated\s*effect\s*size",

    # Explicit hallucination markers
    r"this\s*reference\s*was\s*generated",
    r"fictional\s*reference",
]

MAX_RESPONSE_LENGTH = 100000


def validate_response(text: str) -> bool:
    """
    Returns True if response appears safe.
    Returns False if suspicious fabricated
    research content is detected.
    """

    if not text:
        return False

    if len(text) > MAX_RESPONSE_LENGTH:
        return False

    response = " ".join(
        text.lower().split()
    )

    for pattern in FORBIDDEN_PATTERNS:

        if re.search(pattern, response):
            return False

    return True
