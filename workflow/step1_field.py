import streamlit as st

from modules.idea_validator import (
    validate_research_idea
)


def recommend_study_design(
    data_source,
    outcome,
    default_design="Cross-Sectional Study"
):

    outcome = outcome.lower()

    if data_source == "Registry Database":

        if any(
            x in outcome
            for x in [
                "trend",
                "incidence",
                "prevalence",
                "distribution"
            ]
        ):

            return (
                "Retrospective Registry-Based Study",
                [
                    "Cross-Sectional Study",
                    "Retrospective Cohort Study"
                ]
            )

        return (
            "Retrospective Cohort Study",
            [
                "Cross-Sectional Study"
            ]
        )

    if data_source == "Hospital Records":

        return (
            "Retrospective Cohort Study",
            [
                "Case-Control Study",
                "Cross-Sectional Study"
            ]
        )

    if data_source == "Literature Only":

        return (
            "Systematic Review",
            [
                "Meta-Analysis"
            ]
        )

    return (
        default_design,
        []
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

VALID_DESIGNS = {
    "Registry Database": [
        "Cross-Sectional Study",
        "Case-Control Study",
        "Cohort Study",
    ],
    "Hospital Records": [
        "Cross-Sectional Study",
        "Case-Control Study",
        "Cohort Study",
        "Case Series",
    ],
    "Literature Only": [
        "Systematic Review",
        "Meta-Analysis",
    ],
}

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


def render():

    st.header("🧭 Research Context & Scope")

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

    # ==================================
    # Study Design Validation
    # ==================================

    allowed_designs = VALID_DESIGNS.get(
        data_source,
        STUDY_DESIGNS
    )

    if study_design not in allowed_designs:

        st.error(
            f"""
❌ Selected study design is not compatible
with the chosen data source.

Data Source:
{data_source}

Allowed Designs:
{", ".join(allowed_designs)}
"""
        )

    disease = st.text_input(
        "Disease / Research Topic",
        placeholder="Cancer, Diabetes, Stroke..."
    )

    location = st.text_input(
        "Study Location",
        placeholder="Sana'a, Yemen"
    )

    outcome = st.text_input(
        "Primary Outcome",
        placeholder="Incidence, Mortality, Survival, Risk Factors..."
    )

    recommended_design = None
    alternative_designs = []

    if outcome:

        recommended_design, alternative_designs = (
            recommend_study_design(
                data_source,
                outcome,
                default_design=study_design
            )
        )

    study_period = st.text_input(
        "Study Period",
        placeholder="2015-2025"
    )

    keywords = st.text_area(
        "Initial Keywords",
        placeholder=FIELD_KEYWORD_HINTS.get(
            field,
            "Enter important keywords"
        ),
    )

    # ==================================
    # Auto Research Title
    # ==================================

    if all([
        disease,
        location,
        outcome,
        study_period
    ]):

        generated_title = (
            f"{outcome} of {disease} in "
            f"{location} ({study_period})"
        )

        st.markdown("### Suggested Research Title")

        st.success(
            generated_title
        )

        st.session_state[
            "generated_title"
        ] = generated_title

    # ==================================
    # Draft Research Question
    # ==================================

    if all([
        disease,
        location,
        outcome,
        study_period
    ]):

        draft_question = (
            f"What are the patterns of "
            f"{outcome.lower()} among "
            f"{population.lower()} with "
            f"{disease.lower()} in "
            f"{location} during "
            f"{study_period}?"
        )

        st.markdown(
            "### Draft Research Question"
        )

        st.info(
            draft_question
        )

        st.session_state[
            "draft_research_question"
        ] = draft_question

    context = {
        "field": field,
        "population": population,
        "study_design": study_design,
        "data_source": data_source,
        "disease": disease,
        "location": location,
        "outcome": outcome,
        "study_period": study_period,
        "keywords": keywords,
        "generated_title": st.session_state.get(
            "generated_title",
            ""
        ),
        "draft_research_question": st.session_state.get(
            "draft_research_question",
            ""
        ),
    }

    st.session_state["research_context"] = context

    validation = validate_research_idea(
        study_design,
        data_source
    )

    if recommended_design:

        st.markdown("---")

        st.subheader(
            "📚 Methodology Recommendation"
        )

        st.success(
            f"""
Recommended Design:

{recommended_design}
"""
        )

        if alternative_designs:

            st.info(
                "Alternative Designs:\n\n• "
                + "\n• ".join(
                    alternative_designs
                )
            )

    if (
        recommended_design
        and study_design
        and study_design != recommended_design
    ):

        st.warning(
            f"""
The selected study design differs
from the recommended methodology.

Recommended:
{recommended_design}

Selected:
{study_design}
"""
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

                st.write(f"• {note}")

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

**Disease / Topic:** {disease if disease else 'Not specified'}

**Study Location:** {location if location else 'Not specified'}

**Primary Outcome:** {outcome if outcome else 'Not specified'}

**Study Period:** {study_period if study_period else 'Not specified'}

**Keywords:** {keywords if keywords else 'Not specified'}
"""
    )

    required_fields = [
        disease,
        location,
        outcome,
        study_period,
        keywords
    ]

    if all(str(x).strip() for x in required_fields):

        if st.button(
            "💾 Save Research Context",
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
            "Please complete Disease, Location, Outcome, Study Period and Keywords."
        )

    if st.session_state.get(
        "context_completed"
    ):

        st.success(
            "✅ Step 1 Completed"
        )
