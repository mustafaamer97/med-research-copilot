import streamlit as st


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
