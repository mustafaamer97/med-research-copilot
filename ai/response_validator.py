FORBIDDEN_OUTPUTS = [
    "fake doi",
    "fake pmid",
    "fabricated reference"
]


def validate_response(text):

    response = text.lower()

    for item in FORBIDDEN_OUTPUTS:

        if item in response:
            return False

    return True
