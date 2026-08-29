import re

# ---------------------------------------------------------------------------
# 1. Knowledge Base Configuration
# ---------------------------------------------------------------------------

FIELD_RULES = {
    "Oncology": {
        "keywords": [
            "cancer", "tumor", "tumour", "neoplasm", "leukemia",
            "lymphoma", "melanoma", "carcinoma", "sarcoma", "oncology"
        ],
        "default_population": "Patients diagnosed with malignant neoplasms",
        "domain_keywords": ["Survival Rate", "Mortality", "Chemotherapy", "Oncology", "Tumor Markers"]
    },
    "Cardiology": {
        "keywords": [
            "heart", "cardiac", "myocardial", "coronary", "heart failure",
            "hypertension", "arrhythmia", "atherosclerosis", "cardiology"
        ],
        "default_population": "Patients with cardiovascular conditions",
        "domain_keywords": ["Cardiovascular Outcomes", "Mortality", "Ejection Fraction", "Hypertension", "Lipid Profile"]
    },
    "Neurology": {
        "keywords": [
            "stroke", "epilepsy", "brain", "parkinson", "alzheimer",
            "neurological", "dementia", "seizure", "neurology"
        ],
        "default_population": "Patients with neurological disorders",
        "domain_keywords": ["Cognitive Function", "Neurological Deficit", "Brain MRI", "Functional Recovery", "Seizure Frequency"]
    },
    "Endocrinology": {
        "keywords": [
            "diabetes", "thyroid", "endocrine", "obesity", "insulin",
            "metabolic", "hyperthyroidism", "hypothyroidism", "endocrinology"
        ],
        "default_population": "Patients with endocrine and metabolic disorders",
        "domain_keywords": ["HbA1c", "Glycemic Control", "Insulin Resistance", "Metabolic Syndrome", "Endocrine Function"]
    },
    "Pulmonology": {
        "keywords": [
            "asthma", "copd", "lung disease", "respiratory", "pneumonia",
            "pulmonary", "bronchitis", "pulmonology"
        ],
        "default_population": "Patients with respiratory conditions",
        "domain_keywords": ["Lung Function", "FEV1", "Exacerbation Rate", "Oxygen Saturation", "Respiratory Mechanics"]
    },
    "Nephrology": {
        "keywords": [
            "kidney", "renal", "ckd", "dialysis", "nephritis",
            "creatinine", "nephrology"
        ],
        "default_population": "Patients with renal dysfunction or chronic kidney disease",
        "domain_keywords": ["eGFR", "Serum Creatinine", "Proteinuria", "Dialysis Outcomes", "Renal Survival"]
    },
    "Gastroenterology": {
        "keywords": [
            "hepatitis", "liver", "colon", "gastric", "ibd",
            "cirrhosis", "gastrointestinal", "gastroenterology"
        ],
        "default_population": "Patients with gastrointestinal or hepatic diseases",
        "domain_keywords": ["Liver Enzymes", "Endoscopic Findings", "Mucosal Healing", "Gut Microbiota", "Disease Activity Index"]
    },
    "Psychiatry": {
        "keywords": [
            "depression", "anxiety", "mental health", "psychiatric",
            "bipolar", "schizophrenia", "psychosis", "psychiatry"
        ],
        "default_population": "Patients with psychiatric conditions",
        "domain_keywords": ["Symptom Severity", "Psychometric Scale", "Mental Health Score", "Treatment Response", "Relapse Rate"]
    },
    "Infectious Diseases": {
        "keywords": [
            "covid", "infection", "tuberculosis", "hiv", "malaria",
            "sepsis", "bacterial", "viral", "antimicrobial", "infectious"
        ],
        "default_population": "Patients diagnosed with infectious diseases",
        "domain_keywords": ["Viral Load", "Pathogen Clearance", "Infection Rate", "Antimicrobial Resistance", "Inflammatory Markers"]
    },
}

GOAL_DESIGN_MAP = {
    "trend analysis": {
        "primary": "Retrospective Registry-Based Study",
        "alternatives": ["Cross-Sectional Study", "Time-Series Analysis"],
        "category": "Epidemiology"
    },
    "incidence": {
        "primary": "Retrospective Cohort Study",
        "alternatives": ["Prospective Cohort Study", "Registry-Based Study"],
        "category": "Epidemiology"
    },
    "prevalence": {
        "primary": "Cross-Sectional Study",
        "alternatives": ["Epidemiological Survey", "Retrospective Registry-Based Study"],
        "category": "Epidemiology"
    },
    "risk factors": {
        "primary": "Case-Control Study",
        "alternatives": ["Retrospective Cohort Study", "Cross-Sectional Study"],
        "category": "Epidemiology"
    },
    "treatment outcomes": {
        "primary": "Retrospective Cohort Study",
        "alternatives": ["Prospective Cohort Study", "Randomized Controlled Trial"],
        "category": "Primary Clinical Research"
    },
    "survival analysis": {
        "primary": "Retrospective Cohort Study",
        "alternatives": ["Prospective Cohort Study", "Survival Analysis Model"],
        "category": "Primary Clinical Research"
    },
    "diagnostic accuracy": {
        "primary": "Diagnostic Accuracy Study",
        "alternatives": ["Cross-Sectional Study", "ROC Analysis Study"],
        "category": "Diagnostic Research"
    },
    "prediction model": {
        "primary": "Prediction Model Study",
        "alternatives": ["Retrospective Cohort Study", "Machine Learning Validation"],
        "category": "Prediction Research"
    },
    "systematic review": {
        "primary": "Systematic Review and Meta-Analysis",
        "alternatives": ["Scoping Review", "Narrative Review"],
        "category": "Evidence Synthesis"
    },
}

EHR_DATA_SOURCES = [
    "Hospital Records",
    "Electronic Health Records (EHR)",
    "Registry Database",
    "Clinical Database"
]

STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "from", "involving",
    "study", "analysis", "evaluation", "assessment", "patients", "among",
    "using", "role", "effect", "impact", "association", "between"
}


# ---------------------------------------------------------------------------
# 2. Core Detection & Logic Functions
# ---------------------------------------------------------------------------

def detect_specialty(topic: str) -> tuple[str, int]:
    """Detects medical specialty and calculates match confidence score."""
    text = topic.lower()
    best_field = "General Medicine"
    max_matches = 0

    for field, data in FIELD_RULES.items():
        matches = sum(1 for kw in data["keywords"] if kw in text)
        if matches > max_matches:
            max_matches = matches
            best_field = field

    if max_matches == 0:
        confidence = 50
    elif max_matches == 1:
        confidence = 85
    else:
        confidence = min(98, 85 + (max_matches - 1) * 5)

    return best_field, confidence


def detect_population(topic: str, data_source: str, field: str) -> str:
    """Determines patient population dynamically based on field rules or data source."""
    if field in FIELD_RULES:
        return FIELD_RULES[field]["default_population"]

    if data_source in ["Survey / Questionnaire", "Public Health Data"]:
        return "General Population"

    return "Study Cohort / Hospital Patients"


def recommend_design(goal: str, data_source: str) -> tuple[str, list[str], str]:
    """Recommends primary and alternative study designs alongside research category."""
    goal_key = goal.lower().strip()
    
    if goal_key in GOAL_DESIGN_MAP:
        mapping = GOAL_DESIGN_MAP[goal_key]
        primary = mapping["primary"]
        alternatives = list(mapping["alternatives"])
        category = mapping["category"]

        # Contextual modification based on data source
        if goal_key == "risk factors" and data_source in EHR_DATA_SOURCES:
            primary = "Retrospective Cohort Study"
            alternatives = ["Case-Control Study", "Cross-Sectional Study"]

        return primary, alternatives, category

    # Default fallbacks when goal is unrecognized
    if data_source == "Published Literature" or goal_key == "systematic review":
        return "Systematic Review and Meta-Analysis", ["Scoping Review", "Narrative Review"], "Evidence Synthesis"

    if data_source in EHR_DATA_SOURCES:
        return "Retrospective Cohort Study", ["Case-Control Study", "Cross-Sectional Study"], "Primary Clinical Research"

    return "Cross-Sectional Study", ["Case-Control Study", "Retrospective Cohort Study"], "Primary Clinical Research"


def generate_keywords(topic: str, field: str, goal: str) -> list[str]:
    """Extracts meaningful topic keywords and enriches them with field-specific concepts."""
    raw_words = re.findall(r"[A-Za-z0-9\-]+", topic)
    extracted = []
    
    for word in raw_words:
        w_lower = word.lower()
        if len(w_lower) > 2 and w_lower not in STOP_WORDS and word not in extracted:
            extracted.append(word.capitalize())

    domain_additions = FIELD_RULES.get(field, {}).get("domain_keywords", [])

    combined = []
    for item in extracted + domain_additions + [goal.title()]:
        if item and item not in combined:
            combined.append(item)

    return combined[:10]


# ---------------------------------------------------------------------------
# 3. Main Master Function
# ---------------------------------------------------------------------------

def analyze_research_topic(topic: str, goal: str, data_source: str) -> dict:
    """Master analytical routine for processing research topic parameters."""
    field, confidence = detect_specialty(topic)
    population = detect_population(topic, data_source, field)
    rec_design, alt_designs, research_category = recommend_design(goal, data_source)
    keywords = generate_keywords(topic, field, goal)

    return {
        "field": field,
        "confidence": confidence,
        "population": population,
        "recommended_design": rec_design,
        "alternative_designs": alt_designs,
        "research_category": research_category,
        "keywords": keywords,
    }
