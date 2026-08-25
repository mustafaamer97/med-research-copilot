import streamlit as st


def render_step7():

    st.header(
        "🛡️ Ethics & IRB Preparation"
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

    if st.button(
        "Save IRB Plan"
    ):

        st.session_state[
            "irb_package"
        ] = {
            "risk": study_risk,
            "consent": informed_consent,
            "vulnerable": vulnerable_population
        }

        st.session_state[
            "irb_completed"
        ] = True

        st.success(
            "IRB package saved."
        )

    if st.session_state.get(
        "irb_completed"
    ):
        st.success(
            "✅ Step 7 Completed"
        )
