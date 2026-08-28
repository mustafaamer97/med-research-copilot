import re


# ============================================================
# Medical Specialty Detection
# ============================================================

SPECIALTY_MAP = {

    "oncology": [
        "cancer",
        "tumor",
        "tumour",
        "neoplasm",
        "leukemia",
        "lymphoma",
        "melanoma",
        "carcinoma",
        "sarcoma",
    ],

    "cardiology": [
        "heart",
        "cardiac",
        "myocardial",
        "coronary",
        "heart failure",
        "hypertension",
    ],

    "neurology": [
        "stroke",
        "epilepsy",
        "brain",
        "parkinson",
        "alzheimer",
        "neurological",
    ],

    "endocrinology": [
        "diabetes",
        "thyroid",
        "endocrine",
        "obesity",
        "insulin",
    ],

    "pulmonology": [
        "asthma",
        "copd",
        "lung disease",
        "respiratory",
    ],

    "nephrology": [
        "kidney",
        "renal",
        "ckd",
        "dialysis",
    ],

    "gastroenterology": [
        "hepatitis",
        "liver",
        "colon",
        "gastric",
        "ibd",
    ],

    "psychiatry": [
        "depression",
        "anxiety",
        "mental health",
        "psychiatric",
    ],

    "infectious diseases": [
        "covid",
        "infection",
        "tuberculosis",
        "hiv",
        "malaria",
    ],
}


# ============================================================
# Goal → Default Design
# ============================================================

GOAL_DESIGN_MAP = {

    "trend analysis":
        "Retrospective Cohort Study",

    "incidence":
        "Retrospective Cohort Study",

    "prevalence":
        "Cross-Sectional Study",

    "risk factors":
        "Case-Control Study",

    "treatment outcomes":
        "Retrospective Cohort Study",

    "survival analysis":
        "Retrospective Cohort Study",

    "diagnostic accuracy":
        "Diagnostic Accuracy Study",

    "prediction model":
        "Prediction Model Study",

    "systematic review":
        "Systematic Review",
}


# ============================================================
# Specialty
# ============================================================

def detect_specialty(topic):

    text = str(topic or "").lower().strip()

    for specialty, keywords in SPECIALTY_MAP.items():

        for keyword in keywords:

            if keyword in text:

                return specialty.title()

    return "General Medicine"


# ============================================================
# Keywords
# ============================================================

def generate_keywords(topic):

    text = str(topic or "")

    words = re.findall(
        r"[A-Za-z0-9\-]+",
        text
    )

    stop_words = {
        "the",
        "and",
        "with",
        "from",
        "among",
        "study",
        "patients",
        "patient",
        "disease",
        "effect",
        "outcome",
        "outcomes",
    }

    keywords = []

    for word in words:

        word = word.strip().lower()

        if len(word) < 3:
            continue

        if word in stop_words:
            continue

        if word not in keywords:

            keywords.append(word)

    return keywords[:15]


# ============================================================
# Population Detection
# ============================================================

def detect_population(
    topic,
    data_source,
):

    text = str(topic or "").lower()

    if any(
        x in text
        for x in [
            "cancer",
            "tumor",
            "tumour",
            "neoplasm",
        ]
    ):

        return (
            "Patients diagnosed "
            "with malignant neoplasms"
        )

    if "diabetes" in text:

        return (
            "Patients with diabetes"
        )

    if "stroke" in text:

        return (
            "Patients with stroke"
        )

    if data_source == "Survey / Questionnaire":

        return "General Population"

    return "Study Population"


# ============================================================
# Default Design Recommendation
# ============================================================

def recommend_design(
    goal,
    data_source,
):

    goal_text = str(
        goal or ""
    ).lower().strip()

    source_text = str(
        data_source or ""
    ).strip()

    if goal_text in GOAL_DESIGN_MAP:

        return GOAL_DESIGN_MAP[
            goal_text
        ]

    if source_text in [
        "Registry Database",
        "Hospital Records",
        "Electronic Health Records (EHR)",
    ]:

        return (
            "Retrospective Cohort Study"
        )

    if source_text == "Published Literature":

        return "Systematic Review"

    if source_text == "Survey / Questionnaire":

        return "Cross-Sectional Study"

    return "Cross-Sectional Study"


# ============================================================
# Main Research Topic Analysis
# ============================================================

def analyze_research_topic(
    topic,
    goal,
    data_source,
):

    topic = str(
        topic or ""
    ).strip()

    return {

        "field":
        detect_specialty(
            topic
        ),

        "population":
        detect_population(
            topic,
            data_source,
        ),

        "recommended_design":
        recommend_design(
            goal,
            data_source,
        ),

        "keywords":
        generate_keywords(
            topic
        ),
    }
