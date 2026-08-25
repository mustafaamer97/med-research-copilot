import streamlit as st

STUDY_DESIGNS = [
    "Randomized Controlled Trial (RCT)",
    "Pragmatic Clinical Trial",
    "Prospective Cohort Study",
    "Retrospective Cohort Study",
    "Case-Control Study",
    "Nested Case-Control Study",
    "Cross-Sectional Study",
    "Diagnostic Accuracy Study",
    "Prediction Model Study",
    "Prognostic Study",
    "Survey Study",
    "Case Report",
    "Case Series",
    "Systematic Review",
    "Meta-Analysis",
    "Scoping Review",
    "Umbrella Review",
    "Network Meta-Analysis",
]

from modules.protocol_builder import generate_protocol


def render():

    st.info(
        "Workflow validation is temporarily disabled during development."
    )

    st.header(
        "📋 Research Protocol Builder"
    )

    idea = st.text_area(
        "Enter research idea"
    )

    study_type = st.selectbox(
        "Study Type",
        STUDY_DESIGNS
    )

    if st.button(
        "Generate Protocol"
    ):

        with st.spinner(
            "Building protocol..."
        ):

            protocol = generate_protocol(
                idea,
                study_type
            )

        st.markdown(
            protocol
        )
