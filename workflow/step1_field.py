import streamlit as st

from modules.idea_validator import (
    validate_research_idea
)

MEDICAL_FIELDS = [
    "Cardiology",
    "Neurology",
    "Oncology",
    "Endocrinology",
    "Gastroenterology",
    "Pulmonology",
    "Nephrology",
    "Infectious Diseases",
    "Psychiatry",
    "Dermatology",
    "Pediatrics",
    "Obstetrics & Gynecology",
    "General Surgery",
    "Orthopedic Surgery",
    "Neurosurgery",
    "Urology",
    "Ophthalmology",
    "Otolaryngology (ENT)",
    "Emergency Medicine",
    "Public Health",
]

TARGET_POPULATIONS = [
    "Adults",
    "Children",
    "Elderly",
    "Pregnant Women",
    "General Population",
]

STUDY_DESIGNS = [
    "Cross-Sectional Study",
    "Case-Control Study",
    "Cohort Study",
    "Randomized Controlled Trial (RCT)",
    "Systematic Review",
    "Meta-Analysis",
    "Case Report",
    "Case Series",
    "Diagnostic Study",
    "Survey Study",
]

DATA_SOURCES = [
    "Primary Data",
    "Hospital Records",
    "Registry Database",
    "Literature Only",
]

FIELD_KEYWORD_HINTS = {
    "Cardiology": "heart failure, NT-proBNP, ejection fraction, mortality",
    "Neurology": "stroke, epilepsy, cognition, MRI",
    "Oncology": "survival, chemotherapy, tumor markers",
    "Endocrinology": "diabetes, HbA1c, insulin resistance",
    "Gastroenterology": "IBD, colonoscopy, liver disease",
    "Pulmonology": "COPD, asthma, spirometry",
    "Nephrology": "CKD, dialysis, eGFR",
    "Infectious Diseases": "COVID-19, sepsis, antimicrobial resistance",
    "Psychiatry": "depression, anxiety, quality of life",
    "Dermatology": "psoriasis, eczema, skin lesions",
    "Pediatrics": "growth, vaccination, childhood disease",
    "Obstetrics & Gynecology": "pregnancy outcomes, infertility",
    "General Surgery": "postoperative complications, wound infection",
    "Orthopedic Surgery": "fractures, arthroplasty, outcomes",
    "Neurosurgery": "brain tumors, spinal surgery",
    "Urology": "prostate cancer, kidney stones",
    "Ophthalmology": "glaucoma, cataract, visual acuity",
    "Otolaryngology (ENT)": "hearing loss, sinusitis",
    "Emergency Medicine": "triage, trauma, emergency care",
    "Public Health": "prevalence, risk factors, screening",
}

def render_step1():

    st.header("Step 1: Research Context & Scope")

    st.write(
        "Define your research area before building the research question."
    )

    field = st.selectbox(
        "Main Medical Field",
        MEDICAL_FIELDS
    )

    population = st.selectbox(
        "Target Population",
        TARGET_POPULATIONS
    )

    study_design = st.selectbox(
        "Study Design",
        STUDY_DESIGNS
    )

    data_source = st.selectbox(
        "Available Data Source",
        DATA_SOURCES
    )

    keywords = st.text_area(
        "Initial Keywords",
        placeholder=FIELD_KEYWORD_HINTS.get(
            field,
            "Enter important keywords"
        ),
    )

    context = {
        "field": field,
        "population": population,
        "study_design": study_design,
        "data_source": data_source,
        "keywords": keywords,
    }

    st.session_state["research_context"] = context

    # =========================
    # Feasibility Assessment
    # =========================

    validation = validate_research_idea(
        study_design,
        data_source
    )

    st.markdown("---")

    st.subheader(
        "Research Feasibility Assessment"
    )

    if validation["feasibility"] == "High":

        st.success(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: HIGH
"""
        )

    elif validation["feasibility"] == "Moderate":

        st.warning(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: MODERATE
"""
        )

    else:

        st.error(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: LOW
"""
        )

    if validation["notes"]:

        with st.expander(
            "Why was this score assigned?"
        ):

            for note in validation["notes"]:

                st.write(
                    f"• {note}"
                )

    # =========================
    # Research Context Summary
    # =========================

    st.markdown("---")

    st.subheader(
        "Research Context Summary"
    )

    st.info(
        f"""
**Medical Field:** {field}

**Target Population:** {population}

**Study Design:** {study_design}

**Data Source:** {data_source}

**Keywords:** {keywords if keywords else 'Not specified'}
"""
    )

    # =========================
    # Continue Button
    # =========================

    if keywords.strip():

        if st.button(
            "Save Context & Go to Idea Generator ➜",
            use_container_width=True,
            type="primary",
        ):

            st.session_state[
                "context_completed"
            ] = True

            st.success(
                "Research context saved successfully."
            )

    else:

        st.warning(
