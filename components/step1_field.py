import streamlit as st


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


def render_step1():

    st.header("Step 1: Research Context & Scope")

    st.write("Define your research area before building the question.")

    field = st.selectbox("Main Medical Field", MEDICAL_FIELDS)

    population = st.selectbox("Target Population", TARGET_POPULATIONS)

    study_design = st.selectbox("Study Design", STUDY_DESIGNS)

    data_source = st.selectbox("Available Data Source", DATA_SOURCES)

    keywords = st.text_area(
        "Initial Keywords", placeholder="diabetes, insulin resistance, obesity"
    )

    context = {
        "field": field,
        "population": population,
        "study_design": study_design,
        "data_source": data_source,
        "keywords": keywords,
    }

    st.session_state["research_context"] = context

    st.success(
        f"""
        Research Context Ready

        Field: {field}

        Population: {population}

        Study Design: {study_design}

        Data Source: {data_source}
        """
    )

    return context
