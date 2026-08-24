STUDY_DESIGN_PATTERNS = {

    "Randomized Controlled Trial": [
        "randomized controlled trial",
        "randomised controlled trial",
        "randomized trial",
        "randomised trial"
    ],

    "Cohort Study": [
        "cohort study",
        "prospective cohort",
        "retrospective cohort"
    ],

    "Case-Control Study": [
        "case-control study",
        "case control study"
    ],

    "Cross-Sectional Study": [
        "cross-sectional",
        "cross sectional study"
    ],

    "Systematic Review": [
        "systematic review"
    ],

    "Meta-analysis": [
        "meta-analysis",
        "meta analysis"
    ]
}

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


def detect_study_design(text):

    lower_text = text.lower()

    for design, patterns in (
        STUDY_DESIGN_PATTERNS.items()
    ):

        for pattern in patterns:

            if pattern in lower_text:

                return design

    return "Not detected"


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

    sections["Study Design"] = (
        detect_study_design(text)
    )

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
