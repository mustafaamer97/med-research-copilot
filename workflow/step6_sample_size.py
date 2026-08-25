import streamlit as st


STUDY_TYPES = [
    "Randomized Controlled Trial (RCT)",
    "Prospective Cohort",
    "Retrospective Cohort",
    "Case-Control",
    "Cross-Sectional",
    "Diagnostic Study",
]
    

def render():

    st.header(
        "📊 Sample Size & Statistical Power"
    )

    st.info(
        """
Estimate the required sample size
before starting data collection.
"""
    )

    study_type = st.selectbox(
        "Study Type",
        STUDY_TYPES
    )

    effect_size = st.number_input(
        "Expected Effect Size",
        min_value=0.10,
        max_value=5.00,
        value=0.50,
        step=0.10
    )

    alpha = st.number_input(
        "Alpha (Type I Error)",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01
    )

    power = st.number_input(
        "Statistical Power",
        min_value=0.50,
        max_value=0.99,
        value=0.80,
        step=0.05
    )

    st.markdown("---")

    if st.button(
        "💾 Save Sample Size Plan",
        use_container_width=True,
        type="primary"
    ):

        st.session_state[
            "sample_size_plan"
        ] = {
            "study_type": study_type,
            "effect_size": effect_size,
            "alpha": alpha,
            "power": power,
        }

        st.session_state[
            "sample_size_completed"
        ] = True

        st.success(
            "Sample size plan saved successfully."
        )

    if st.session_state.get(
        "sample_size_plan"
    ):

        st.subheader(
            "Current Sample Size Plan"
        )

        st.json(
            st.session_state[
                "sample_size_plan"
            ]
        )

    if st.session_state.get(
        "sample_size_completed"
    ):

        st.success(
            "✅ Step 6 Completed"
        )
