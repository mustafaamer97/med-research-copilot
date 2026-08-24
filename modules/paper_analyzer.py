SECTION_KEYWORDS = {

    "Objective": [
        "objective",
        "background",
        "aim",
        "purpose"
    ],

    "Methods": [
        "methods",
        "methodology",
        "materials and methods"
    ],

    "Results": [
        "results",
        "findings"
    ],

    "Conclusion": [
        "conclusion",
        "conclusions"
    ],

    "Limitations": [
        "limitations",
        "strengths and limitations"
    ]
}


def analyze_paper(text):

    sections = {

        "Title": "",
        "Objective": "",
        "Study Design": "",
        "Population": "",
        "Methods": "",
        "Results": "",
        "Conclusion": "",
        "Limitations": ""

    }

    lower_text = text.lower()

    for section_name, keywords in SECTION_KEYWORDS.items():

        for keyword in keywords:

            if keyword in lower_text:

                sections[
                    section_name
                ] = extract_section(
                    text,
                    keyword
                )

                break

    return sections


def extract_section(text, keyword):

    start = text.lower().find(keyword)

    end = start + 1500

    return text[start:end].strip()
