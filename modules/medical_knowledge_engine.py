import re

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

GOAL_DESIGN_MAP = {
    "trend analysis": "Retrospective Registry-Based Study",
    "incidence": "Retrospective Registry-Based Study",
    "prevalence": "Cross-Sectional Study",
    "treatment outcomes": "Retrospective Cohort Study",
    "survival analysis": "Retrospective Cohort Study",
    "diagnostic accuracy": "Diagnostic Accuracy Study",
    "prediction model": "Prediction Model Study",
    "systematic review": "Systematic Review",
}


def detect_specialty(topic):

    text = topic.lower()

    for specialty, keywords in SPECIALTY_MAP.items():

        for keyword in keywords:

            if keyword in text:

                return specialty.title()

    return "General Medicine"


def generate_keywords(topic):

    words = re.findall(
        r"[A-Za-z0-9\-]+",
        topic
    )

    words = [
        w.strip()
        for w in words
        if len(w) > 2
    ]

    unique_words = []

    for word in words:

        if word not in unique_words:

            unique_words.append(word)

    return unique_words[:15]


def detect_population(
    topic,
    data_source,
):

    topic = topic.lower()

    if any(
        x in topic
        for x in [
            "cancer",
            "tumor",
            "neoplasm",
        ]
    ):
        return (
            "Patients diagnosed "
            "with malignant neoplasms"
        )

    if "diabetes" in topic:

        return (
            "Patients with diabetes"
        )

    if "stroke" in topic:

        return (
            "Patients with stroke"
        )

    if data_source == "Survey / Questionnaire":

        return "General Population"

    return "Study Population"


def recommend_design(
    goal,
    data_source,
):

    goal = goal.lower()

    if goal == "risk factors":

        if data_source in [
            "Hospital Records",
            "Electronic Health Records (EHR)",
            "Registry Database"
        ]:

            return (
                "Retrospective Cohort Study"
            )

        return (
            "Case-Control Study"
        )

    if goal in GOAL_DESIGN_MAP:

        return GOAL_DESIGN_MAP[goal]

    if data_source in [
        "Registry Database",
        "Hospital Records",
        "Electronic Health Records (EHR)",
    ]:

        return (
            "Retrospective Cohort Study"
        )

    return (
        "Cross-Sectional Study"
    )


def detect_research_category(
    data_source,
    goal,
    study_design
):

    goal = goal.lower()

    if study_design in [
        "Systematic Review",
        "Meta-Analysis",
        "Network Meta-Analysis",
        "Scoping Review",
        "Umbrella Review"
    ]:

        return "Evidence Synthesis"

    if data_source == "Published Literature":

        return "Secondary Research"

    return "Primary Research"


def analyze_research_topic(
    topic,
    goal,
    data_source,
):

    return {

        "field":
        detect_specialty(topic),

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

        "research_category":
        detect_research_category(
            data_source,
            goal,
            recommend_design(
                goal,
                data_source
            )
        ),

        "keywords":
        generate_keywords(topic),
    }
