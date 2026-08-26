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

    sample_plan = st.session_state.get(
        "sample_size_plan",
        {}
    )

    default_sample_size = sample_plan.get(
        "total_sample",
        100
    )

    expected_sample_size = st.number_input(
        "Expected Sample Size",
        min_value=1,
        value=int(default_sample_size)
    )

    # ==================================
    # Variable Classification
    # ==================================

    st.subheader(
        "Variable Classification"
    )

    variable_list = [
        v.strip()
        for v in variables.split("\n")
        if v.strip()
    ]

    demographics = []
    outcomes = []
    exposures = []
    confounders = []

    for var in variable_list:

        lower = var.lower()

        if lower in [
            "age",
            "sex",
            "gender"
        ]:

            demographics.append(var)

        elif any(
            x in lower
            for x in [
                "mortality",
                "death",
                "admission",
                "outcome"
            ]
        ):

            outcomes.append(var)

        elif any(
            x in lower
            for x in [
                "bmi",
                "smoking",
                "treatment",
                "exposure"
            ]
        ):

            exposures.append(var)

        else:

            confounders.append(var)

    c1, c2 = st.columns(2)

    with c1:

        st.write("### Demographics")
        st.write(demographics)

        st.write("### Exposure Variables")
        st.write(exposures)

    with c2:

        st.write("### Outcome Variables")
        st.write(outcomes)

        st.write("### Confounders")
        st.write(confounders)

    # ==================================
    # Feasibility Score
    # ==================================

    score = 100

    if len(variable_list) > 20:

        score -= 20

    if expected_sample_size > 1000:

        score -= 30

    if estimated_duration > 24:

        score -= 20

    st.subheader(
        "Data Collection Feasibility"
    )

    st.progress(
        score / 100
    )

    if score >= 80:

        st.success(
            "Easy Study"
        )

    elif score >= 50:

        st.warning(
            "Moderate Complexity"
        )

    else:

        st.error(
            "Complex Study"
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

            "variables":
            variables,

            "method":
            collection_method,

            "duration_months":
            estimated_duration,

            "expected_sample_size":
            expected_sample_size,

            "demographics":
            demographics,

            "outcomes":
            outcomes,

            "exposures":
            exposures,

            "confounders":
            confounders,

            "feasibility_score":
            score
        }

        # ==================================
        # Data Dictionary
        # ==================================

        dictionary = []

        for variable in variable_list:

            dictionary.append(
                {
                    "Variable":
                    variable,

                    "Type":
                    "Numeric",

                    "Required":
                    "Yes"
                }
            )

        st.session_state[
            "data_dictionary"
        ] = dictionary

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
        # Google Forms Preparation
        # ==================================

        st.markdown("---")

        if st.button(
            "🚀 Prepare Google Form",
            use_container_width=True
        ):

            st.session_state[
                "google_form_ready"
            ] = True

            st.success(
                "Questionnaire prepared for Google Forms integration."
            )

        if st.session_state.get(
            "google_form_ready"
        ):

            st.info(
                """
Google Forms integration is configured.

When Google API connection is enabled,
this questionnaire will be converted
into a Google Form automatically.
"""
            )

    # ==================================
    # Data Dictionary
    # ==================================

    if st.session_state.get(
        "data_dictionary"
    ):

        st.subheader(
            "Data Dictionary"
        )

        st.dataframe(
            st.session_state[
                "data_dictionary"
            ],
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
