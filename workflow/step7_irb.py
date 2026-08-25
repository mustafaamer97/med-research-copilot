import streamlit as st


def render():

    st.header(
        "🛡️ Ethics & IRB Preparation"
    )

    st.info(
        """
Prepare the ethical approval requirements
before data collection begins.
"""
    )

    study_risk = st.selectbox(
        "Risk Level",
        [
            "Minimal Risk",
            "Moderate Risk",
            "High Risk"
        ]
    )

    informed_consent = st.checkbox(
        "Informed Consent Required",
        value=True
    )

    vulnerable_population = st.checkbox(
        "Includes Vulnerable Population"
    )

    multicenter_study = st.checkbox(
        "Multicenter Study"
    )

    biological_samples = st.checkbox(
        "Biological Samples Collected"
    )

    patient_identifiers = st.checkbox(
        "Patient Identifiable Data Used"
    )

    st.markdown("---")

    if st.button(
        "💾 Save IRB Package",
        use_container_width=True,
        type="primary"
    ):

        st.session_state[
            "irb_package"
        ] = {
            "risk": study_risk,
            "consent": informed_consent,
            "vulnerable": vulnerable_population,
            "multicenter": multicenter_study,
            "biological_samples": biological_samples,
            "patient_identifiers": patient_identifiers,
        }

        st.session_state[
            "irb_completed"
        ] = True

        st.success(
            "IRB package saved successfully."
        )

    if st.session_state.get(
        "irb_package"
    ):

        st.subheader(
            "Current IRB Package"
        )

        st.json(
            st.session_state[
                "irb_package"
            ]
        )

    if st.session_state.get(
        "irb_completed"
    ):

        st.success(
            "✅ Step 7 Completed"
        )
