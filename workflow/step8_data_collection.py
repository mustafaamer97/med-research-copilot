import streamlit as st

from modules.questionnaire_builder import (
    generate_questionnaire
)

COLLECTION_METHODS = [
    "Survey",
    "Hospital Records",
    "Registry Database",
    "Electronic Health Records (EHR)",
    "Laboratory Data",
    "Clinical Examination",
    "Questionnaire",
    "Imaging Data",
]


def render():

    st.header(
        "📝 Data Collection Plan"
    )

    st.info(
        """
Define how study data will be collected
before starting recruitment.
"""
    )

    research_context = st.session_state.get(
        "research_context",
        {}
    )

    research_question = st.session_state.get(
        "research_question",
        {}
    )

    protocol = st.session_state.get(
        "research_protocol",
        ""
    )

    variables = st.text_area(
        "Variables to Collect",
        height=180,
        placeholder="""
Age
Sex
BMI
Blood Pressure
HbA1c
Mortality
Hospital Admission
"""
    )

    collection_method = st.selectbox(
        "Collection Method",
        COLLECTION_METHODS
    )

    estimated_duration = st.number_input(
        "Estimated Data Collection Duration (Months)",
        min_value=1,
        max_value=120,
        value=6
    )

    expected_sample_size = st.number_input(
        "Expected Sample Size",
        min_value=1,
        value=100
    )

    st.markdown("---")

    if st.button(
        "💾 Save Collection Plan",
        use_container_width=True,
        type="primary"
    ):

        st.session_state[
            "data_collection_plan"
        ] = {
            "variables": variables,
            "method": collection_method,
            "duration_months": estimated_duration,
            "expected_sample_size": expected_sample_size,
        }

        st.session_state[
            "data_collection_completed"
        ] = True

        st.success(
            "Data collection plan saved successfully."
        )

    # ==================================
    # Generate Questionnaire
    # ==================================

    if st.button(
        "📝 Generate Questionnaire",
        use_container_width=True
    ):

        with st.spinner(
            "Generating questionnaire..."
        ):

            questionnaire = generate_questionnaire(
                research_context,
                research_question,
                protocol
            )

        st.session_state[
            "research_questionnaire"
        ] = questionnaire

        st.rerun()

    questionnaire = st.session_state.get(
        "research_questionnaire"
    )

    if questionnaire:

        st.subheader(
            "Generated Questionnaire"
        )

        st.markdown(
            questionnaire
        )

        st.download_button(
            "⬇️ Download Questionnaire",
            data=questionnaire,
            file_name="research_questionnaire.md",
            use_container_width=True
        )

    # ==================================
    # Current Plan Display
    # ==================================

    if st.session_state.get(
        "data_collection_plan"
    ):

        st.subheader(
            "Current Collection Plan"
        )

        st.json(
            st.session_state[
                "data_collection_plan"
            ]
        )

    if st.session_state.get(
        "data_collection_completed"
    ):

        st.success(
            "✅ Step 8 Completed"
        )
