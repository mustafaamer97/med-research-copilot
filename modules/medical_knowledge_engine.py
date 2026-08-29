import re
from functools import lru_cache

# ---------------------------------------------------------------------------
# 1. Constants & Configuration Sets
# ---------------------------------------------------------------------------

DEFAULT_EVIDENCE_SYNTHESIS = "Systematic Review and Meta-Analysis"
MAX_KEYWORDS = 15

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
# 2. Knowledge Base Configuration (with Medical Aliases & Acronyms)
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
            "lymphoma", "melanoma", "carcinoma", "sarcoma", "oncology",
            "nsclc", "sclc", "aml", "cml", "crc", "rcc", "hcc"
        ],
        "default_population": "Patients diagnosed with malignant neoplasms",
        "domain_keywords": ["Survival Rate", "Mortality", "Chemotherapy", "Oncology", "Tumor Markers"],
        "outcomes": ["Overall Survival (OS)", "Progression-Free Survival (PFS)", "Cancer-Specific Mortality"]
    },
    "Cardiology": {
        "keywords": [
            "heart", "cardiac", "myocardial", "coronary", "heart failure",
            "hypertension", "arrhythmia", "atherosclerosis", "cardiology",
            "hf", "chf", "hfref", "hfpef", "acs", "mi", "cad", "afib"
        ],
        "default_population": "Patients with cardiovascular conditions",
        "domain_keywords": ["Cardiovascular Outcomes", "Mortality", "Ejection Fraction", "Hypertension", "Lipid Profile"],
        "outcomes": ["Major Adverse Cardiovascular Events (MACE)", "30-Day Mortality", "Heart Failure Hospitalization"]
    },
    "Neurology": {
        "keywords": [
            "stroke", "epilepsy", "brain", "parkinson", "alzheimer",
            "neurological", "dementia", "seizure", "neurology",
            "tgh", "tbi", "als", "ms", "ich", "sah"
        ],
        "default_population": "Patients with neurological disorders",
        "domain_keywords": ["Cognitive Function", "Neurological Deficit", "Brain MRI", "Functional Recovery", "Seizure Frequency"],
        "outcomes": ["Modified Rankin Scale (mRS) Score", "Stroke Recurrence", "Cognitive Decline Rate"]
    },
    "Endocrinology": {
        "keywords": [
            "diabetes", "thyroid", "endocrine", "obesity", "insulin",
            "metabolic", "hyperthyroidism", "hypothyroidism", "endocrinology",
            "t1dm", "t2dm", "dm", "dka", "pcos", "nash", "masld"
        ],
        "default_population": "Patients with endocrine and metabolic disorders",
        "domain_keywords": ["HbA1c", "Glycemic Control", "Insulin Resistance", "Metabolic Syndrome", "Endocrine Function"],
        "outcomes": ["HbA1c Reduction", "Hypoglycemic Events", "Microvascular Complications"]
    },
    "Pulmonology": {
        "keywords": [
            "asthma", "copd", "lung disease", "respiratory", "pneumonia",
            "pulmonary", "bronchitis", "pulmonology",
            "ipf", "osa", "ards", "ali"
        ],
        "default_population": "Patients with respiratory conditions",
        "domain_keywords": ["Lung Function", "FEV1", "Exacerbation Rate", "Oxygen Saturation", "Respiratory Mechanics"],
        "outcomes": ["Annual Exacerbation Rate", "FEV1 Decline", "All-Cause Mortality"]
    },
    "Nephrology": {
        "keywords": [
            "kidney", "renal", "ckd", "dialysis", "nephritis",
            "creatinine", "nephrology",
            "esrd", "eskd", "aki", "ign", "fsgs"
        ],
        "default_population": "Patients with renal dysfunction or chronic kidney disease",
        "domain_keywords": ["eGFR", "Serum Creatinine", "Proteinuria", "Dialysis Outcomes", "Renal Survival"],
        "outcomes": ["ESRD Progression", "eGFR Decline Rate", "Cardiovascular Mortality in CKD"]
    },
    "Gastroenterology": {
        "keywords": [
            "hepatitis", "liver", "colon", "gastric", "ibd",
            "cirrhosis", "gastrointestinal", "gastroenterology",
            "uc", "cd", "gerd", "nafld", "hcv", "hbv"
        ],
        "default_population": "Patients with gastrointestinal or hepatic diseases",
        "domain_keywords": ["Liver Enzymes", "Endoscopic Findings", "Mucosal Healing", "Gut Microbiota", "Disease Activity Index"],
        "outcomes": ["Endoscopic Remission", "Sustained Virologic Response (SVR)", "Cirrhosis Decompensation"]
    },
    "Psychiatry": {
        "keywords": [
            "depression", "anxiety", "mental health", "psychiatric",
            "bipolar", "schizophrenia", "psychosis", "psychiatry",
            "mdd", "gad", "ptsd", "ocd", "bpd"
        ],
        "default_population": "Patients with psychiatric conditions",
        "domain_keywords": ["Symptom Severity", "Psychometric Scale", "Mental Health Score", "Treatment Response", "Relapse Rate"],
        "outcomes": ["Symptom Remission Rate", "Relapse Rate", "Treatment Adherence"]
    },
    "Infectious Diseases": {
        "keywords": [
            "covid", "infection", "tuberculosis", "hiv", "malaria",
            "sepsis", "bacterial", "viral", "antimicrobial", "infectious",
            "tb", "aids", "mrsa", "vre", "amr"
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

def detect_specialty(topic: str) -> tuple[str, int, list[tuple[str, int]]]:
    """
    Detects medical specialty using word boundary regex.
    Returns: (best_field, confidence_score, candidate_fields)
    """
    text = topic.lower()
    scores = {}

    for field, data in FIELD_RULES.items():
        if field == "General Medicine":
            continue
        
        matches = 0
        for kw in data["keywords"]:
            if re.search(rf"\b{re.escape(kw)}\b", text):
                matches += 1
                
        if matches > 0:
            scores[field] = matches

    if not scores:
        return "General Medicine", 50, [("General Medicine", 0)]

    # Sort fields by number of keyword matches
    sorted_candidates = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_field, max_matches = sorted_candidates[0]

    if max_matches == 1:
        confidence = 85
    else:
        confidence = min(98, 85 + (max_matches - 1) * 5)

    return best_field, confidence, sorted_candidates


def get_confidence_level(score: int) -> str:
    """Returns human-readable text category for confidence score."""
    if score >= 95:
        return "Very High"
    if score >= 85:
        return "High"
    if score >= 60:
        return "Moderate"
        
    return "Unknown"


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
    """Extracts meaningful topic keywords with case-insensitive deduplication and field enrichment."""
    raw_words = re.findall(r"[A-Za-z0-9\-]+", topic)
    extracted = []
    
    for word in raw_words:
        w_lower = word.lower()
        if len(w_lower) > 2 and w_lower not in STOP_WORDS:
            extracted.append(word.capitalize())

    domain_additions = FIELD_RULES.get(field, {}).get("domain_keywords", [])

    combined = []
    seen = set()
    
    for item in extracted + domain_additions + [goal.title()]:
        if item:
            key = item.lower()
            if key not in seen:
                combined.append(item)
                seen.add(key)

    return combined[:MAX_KEYWORDS]


# ---------------------------------------------------------------------------
# 4. Main Master Function (Cached & Guarded)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=200)
def analyze_research_topic(topic: str, goal: str, data_source: str) -> dict:
    """Master analytical routine with LRU cache and empty-input safety guard."""
    clean_topic = (topic or "").strip()
    clean_goal = (goal or "").strip()
    clean_source = (data_source or "").strip()

    # Safety Guard for empty or null input
    if not clean_topic:
        return {
            "field": "General Medicine",
            "confidence": 0,
            "confidence_level": "Unknown",
            "candidate_fields": [("General Medicine", 0)],
            "population": "General Patient Population",
            "population_source": "default",
            "recommended_design": "Cross-Sectional Study",
            "alternative_designs": [],
            "research_category": "General Research",
            "keywords": [],
            "suggested_outcomes": FIELD_RULES["General Medicine"]["outcomes"],
        }

    field, confidence, candidate_fields = detect_specialty(clean_topic)
    population, pop_source = detect_population(clean_source, field)
    rec_design, alt_designs, research_category = recommend_design(clean_goal, clean_source)
    keywords = generate_keywords(clean_topic, field, clean_goal)
    outcomes = FIELD_RULES.get(field, {}).get("outcomes", [])

    return {
        "field": field,
        "confidence": confidence,
        "confidence_level": get_confidence_level(confidence),
        "candidate_fields": candidate_fields,
        "population": population,
        "population_source": pop_source,
        "recommended_design": rec_design,
        "alternative_designs": alt_designs,
        "research_category": research_category,
        "keywords": keywords,
        "suggested_outcomes": outcomes,
    }
