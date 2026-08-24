import streamlit as st


MEDICAL_FIELDS = {
    "Cardiology": [
        "Heart Failure",
        "Arrhythmia",
        "Coronary Artery Disease",
        "Hypertension"
    ],
    "Oncology": [
        "Breast Cancer",
        "Lung Cancer",
        "Colorectal Cancer",
        "Leukemia"
    ],
    "Neurology": [
        "Stroke",
        "Epilepsy",
        "Parkinson Disease",
        "Alzheimer Disease"
    ],
    "Endocrinology": [
        "Diabetes",
        "Thyroid Disorders",
        "Obesity"
    ],
    "Infectious Diseases": [
        "COVID-19",
        "Tuberculosis",
        "Hepatitis",
        "HIV"
    ]
}


STUDY_DESIGNS = {
    "Cross-Sectional":
        "Measures exposure and outcome at one point in time.",
    "Case-Control":
        "Compares patients with disease versus controls.",
    "Cohort":
        "Follows exposed and unexposed groups over time.",
    "RCT":
        "Randomized controlled trial. Highest level for interventions.",
    "Systematic Review":
        "Collects and analyzes all available evidence."
}


def render_step1():

    st.header("Step 1: Research Context & Scope")

    st.write(
        "Define your research area before building the question."
    )

    field = st.selectbox(
        "Main Medical Field",
        list(MEDICAL_FIELDS.keys())
    )

    subspecialty = st.selectbox(
        "Sub-specialty",
        MEDICAL_FIELDS[field]
    )

    population = st.selectbox(
        "Target Population",
        [
            "Adults",
            "Pediatrics",
            "Elderly",
            "Pregnant Women",
            "Inpatients",
            "Outpatients"
        ]
    )

    study_design = st.selectbox(
        "Study Design",
        list(STUDY_DESIGNS.keys())
    )

    with st.expander("Study Design Guide"):

        st.info(
            STUDY_DESIGNS[study_design]
        )

    data_source = st.selectbox(
        "Available Data Source",
        [
            "Primary Data",
            "Hospital Records",
            "Literature Only"
        ]
    )

    keywords = st.text_area(
        "Initial Keywords",
        placeholder="diabetes, insulin resistance, obesity"
    )

    context = {
        "field": field,
        "subspecialty": subspecialty,
        "population": population,
        "study_design": study_design,
        "data_source": data_source,
        "keywords": keywords
    }

    st.session_state["research_context"] = context

    st.success(
        f"""
        Research Context Ready

        Field: {field}

        Sub-specialty: {subspecialty}

        Population: {population}

        Study Design: {study_design}

        Data Source: {data_source}
        """
    )

    return context
