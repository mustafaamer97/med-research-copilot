import streamlit as st


def render_step6():

    st.header(
        "📊 Sample Size & Statistical Power"
    )

    st.info(
        """
This module helps estimate sample size requirements
for future studies.

Currently under development.
"""
    )

    study_type = st.selectbox(
        "Study Type",
        [
            "RCT",
            "Cohort",
            "Case-Control",
            "Cross-Sectional"
        ]
    )

    effect_size = st.number_input(
        "Expected Effect Size",
        min_value=0.1,
        value=0.5,
        step=0.1
    )

    alpha = st.number_input(
        "Alpha",
        min_value=0.01,
        value=0.05,
        step=0.01
    )

    power = st.number_input(
        "Power",
        min_value=0.50,
        value=0.80,
        step=0.05
    )

    if st.button(
        "Save Sample Size Plan"
    ):

        st.session_state[
            "sample_size_plan"
        ] = {
            "study_type": study_type,
            "effect_size": effect_size,
            "alpha": alpha,
            "power": power
        }

        st.session_state[
            "sample_size_completed"
        ] = True

        st.success(
            "Sample size plan saved."
        )

    if st.session_state.get(
        "sample_size_completed"
    ):
        st.success(
            "✅ Step 6 Completed"
        )
