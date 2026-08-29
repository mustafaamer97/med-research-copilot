import re
from functools import lru_cache

# ---------------------------------------------------------------------------
# 1. Constants & Configuration Sets
# ---------------------------------------------------------------------------

DEFAULT_EVIDENCE_SYNTHESIS = "Systematic Review and Meta-Analysis"

EHR_DATA_SOURCES = {
    "Hospital Records",
    "Electronic Health Records (EHR)",
    "Registry Database",
    "Clinical Database"
}

STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "from", "involving",
    "study", "analysis", "evaluation", "assessment", "patients", "among",
    "using", "role", "effect", "impact", "association", "between"
}

# ---------------------------------------------------------------------------
# 2. Knowledge Base Configuration
# ---------------------------------------------------------------------------

FIELD_RULES = {
    "General Medicine": {
        "keywords": [],
        "default_population": "General Patient Population",
        "domain_keywords": ["Clinical Outcomes", "Mortality", "Morbidity"],
        "outcomes": ["Overall Mortality", "Readmission Rate", "Length of Stay"]
    },
    "Oncology": {
        "keywords": [
            "cancer", "tumor", "tumour", "neoplasm", "leukemia",
            "lymphoma", "melanoma", "carcinoma", "sarcoma", "oncology"
        ],
        "default_population": "Patients diagnosed with malignant neoplasms",
        "domain_keywords": ["Survival Rate", "Mortality", "Chemotherapy", "Oncology", "Tumor Markers"],
        "outcomes": ["Overall Survival (OS)", "Progression-Free Survival (PFS)", "Cancer-Specific Mortality"]
    },
    "Cardiology": {
        "keywords": [
            "heart", "cardiac", "myocardial", "coronary", "heart failure",
            "hypertension", "arrhythmia", "atherosclerosis", "cardiology"
        ],
        "default_population": "Patients with cardiovascular conditions",
        "domain_keywords": ["Cardiovascular Outcomes", "Mortality", "Ejection Fraction", "Hypertension", "Lipid Profile"],
        "outcomes": ["Major Adverse Cardiovascular Events (MACE)", "30-Day Mortality", "Heart Failure Hospitalization"]
    },
    "Neurology": {
        "keywords": [
            "stroke", "epilepsy", "brain", "parkinson", "alzheimer",
            "neurological", "dementia", "seizure", "neurology"
        ],
        "default_population": "Patients with neurological disorders",
        "domain_keywords": ["Cognitive Function", "Neurological Deficit", "Brain MRI", "Functional Recovery", "Seizure Frequency"],
        "outcomes": ["Modified Rankin Scale (mRS) Score", "Stroke Recurrence", "Cognitive Decline Rate"]
    },
    "Endocrinology": {
        "keywords": [
            "diabetes", "thyroid", "endocrine", "obesity", "insulin",
            "metabolic", "hyperthyroidism", "hypothyroidism", "endocrinology"
        ],
        "default_population": "Patients with endocrine and metabolic disorders",
        "domain_keywords": ["HbA1c", "Glycemic Control", "Insulin Resistance", "Metabolic Syndrome", "Endocrine Function"],
        "outcomes": ["HbA1c Reduction", "Hypoglycemic Events", "Microvascular Complications"]
    },
    "Pulmonology": {
        "keywords": [
            "asthma", "copd", "lung disease", "respiratory", "pneumonia",
            "pulmonary", "bronchitis", "pulmonology"
        ],
        "default_population": "Patients with respiratory conditions",
        "domain_keywords": ["Lung Function", "FEV1", "Exacerbation Rate", "Oxygen Saturation", "Respiratory Mechanics"],
        "outcomes": ["Annual Exacerbation Rate", "FEV1 Decline", "All-Cause Mortality"]
    },
    "Nephrology": {
        "keywords": [
            "kidney", "renal", "ckd", "dialysis", "nephritis",
            "creatinine", "nephrology"
        ],
        "default_population": "Patients with renal dysfunction or chronic kidney disease",
        "domain_keywords": ["eGFR", "Serum Creatinine", "Proteinuria", "Dialysis Outcomes", "Renal Survival"],
        "outcomes": ["ESRD Progression", "eGFR Decline Rate", "Cardiovascular Mortality in CKD"]
    },
    "Gastroenterology": {
        "keywords": [
            "hepatitis", "liver", "colon", "gastric", "ibd",
            "cirrhosis", "gastrointestinal", "gastroenterology"
        ],
        "default_population": "Patients with gastrointestinal or hepatic diseases",
        "domain_keywords": ["Liver Enzymes", "Endoscopic Findings", "Mucosal Healing", "Gut Microbiota", "Disease Activity Index"],
        "outcomes": ["Endoscopic Remission", "Sustained Virologic Response (SVR)", "Cirrhosis Decompensation"]
    },
    "Psychiatry": {
        "keywords": [
            "depression", "anxiety", "mental health", "psychiatric",
            "bipolar", "schizophrenia", "psychosis", "psychiatry"
        ],
        "default_population": "Patients with psychiatric conditions",
        "domain_keywords": ["Symptom Severity", "Psychometric Scale", "Mental Health Score", "Treatment Response", "Relapse Rate"],
        "outcomes": ["Symptom Remission Rate", "Relapse Rate", "Treatment Adherence"]
    },
    "Infectious Diseases": {
        "keywords": [
            "covid", "infection", "tuberculosis", "hiv", "malaria",
            "sepsis", "bacterial", "viral", "antimicrobial", "infectious"
        ],
        "default_population": "Patients diagnosed with infectious diseases",
        "domain_keywords": ["Viral Load", "Pathogen Clearance", "Infection Rate", "Antimicrobial Resistance", "Inflammatory Markers"],
        "outcomes": ["Pathogen Clearance Time", "30-Day Mortality", "Infection Recurrence Rate"]
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
        "primary": DEFAULT_EVIDENCE_SYNTHESIS,
        "alternatives": ["Scoping Review", "Narrative Review"],
        "category": "Evidence Synthesis"
    },
}

# ---------------------------------------------------------------------------
# 3. Core Logic & Helper Functions
# ---------------------------------------------------------------------------

def detect_specialty(topic: str) -> tuple[str, int]:
    """Detects medical specialty using word boundary regex and calculates match confidence score."""
    text = topic.lower()
    best_field = "General Medicine"
    max_matches = 0

    for field, data in FIELD_RULES.items():
        if field == "General Medicine":
            continue
        
        matches = 0
        for kw in data["keywords"]:
            # Use Regex word boundaries to avoid false substring matching (e.g., heart -> heartburn)
            if re.search(rf"\b{re.escape(kw)}\b", text):
                matches += 1
                
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


def get_confidence_level(score: int) -> str:
    """Returns human-readable text category for confidence score."""
    if score >= 95:
        return "Very High"
    if score >= 85:
        return "High"
        
    return "Moderate"


def detect_population(data_source: str, field: str) -> tuple[str, str]:
    """Determines patient population and returns its source (detected vs default)."""
    if field in FIELD_RULES and field != "General Medicine":
        return FIELD_RULES[field]["default_population"], "detected"

    if data_source in {"Survey / Questionnaire", "Public Health Data"}:
        return "General Population", "detected"

    return FIELD_RULES["General Medicine"]["default_population"], "default"


def recommend_design(goal: str, data_source: str) -> tuple[str, list[str], str]:
    """Recommends primary and alternative study designs alongside research category."""
    goal_key = goal.lower().strip()
    
    if goal_key in GOAL_DESIGN_MAP:
        mapping = GOAL_DESIGN_MAP[goal_key]
        primary = mapping["primary"]
        alternatives = list(mapping["alternatives"])
        category = mapping["category"]

        if goal_key == "risk factors" and data_source in EHR_DATA_SOURCES:
            primary = "Retrospective Cohort Study"
            alternatives = ["Case-Control Study", "Cross-Sectional Study"]

        return primary, alternatives, category

    if data_source == "Published Literature" or goal_key == "systematic review":
        return DEFAULT_EVIDENCE_SYNTHESIS, ["Scoping Review", "Narrative Review"], "Evidence Synthesis"

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

    MAX_KEYWORDS = 15
    return combined[:MAX_KEYWORDS]


# ---------------------------------------------------------------------------
# 4. Main Master Function (Cached)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=200)
def analyze_research_topic(topic: str, goal: str, data_source: str) -> dict:
    """Master analytical routine with LRU cache optimization."""
    field, confidence = detect_specialty(topic)
    population, pop_source = detect_population(data_source, field)
    rec_design, alt_designs, research_category = recommend_design(goal, data_source)
    keywords = generate_keywords(topic, field, goal)
    outcomes = FIELD_RULES.get(field, {}).get("outcomes", [])

    return {
        "field": field,
        "confidence": confidence,
        "confidence_level": get_confidence_level(confidence),
        "population": population,
        "population_source": pop_source,
        "recommended_design": rec_design,
        "alternative_designs": alt_designs,
        "research_category": research_category,
        "keywords": keywords,
        "suggested_outcomes": outcomes,
    }
