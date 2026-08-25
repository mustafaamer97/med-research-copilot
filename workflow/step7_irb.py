import streamlit as st

from modules.ethics_builder import (
    generate_ethics_package
)


def render():

    st.header(
        "🛡️ Ethics & IRB Preparation"
    )

    research_question = (
        st.session_state.get(
            "research_question",
            {}
        )
    )

    research_context = (
        st.session_state.get(
            "research_context",
            {}
        )
    )

    protocol = (
        st.session_state.get(
            "research_protocol",
            ""
        )
    )

    study_type = (
        research_context.get(
            "study_design",
            "Clinical Study"
        )
    )

    st.subheader(
        "IRB Settings"
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

    st.divider()

    if st.button(
        "🛡️ Generate Ethics Package",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "Preparing IRB package..."
        ):

            ethics_package = (
                generate_ethics_package(
                    research_question=
                    research_question.get(
                        "question",
                        ""
                    ),
                    study_type=
                    study_type,
                    risk_level=
                    study_risk,
                    informed_consent=
                    informed_consent,
                    vulnerable_population=
                    vulnerable_population
                )
            )

        st.session_state[
            "ethics_package"
        ] = ethics_package

        st.session_state[
            "irb_package"
        ] = {
            "risk":
            study_risk,

            "consent":
            informed_consent,

            "vulnerable":
            vulnerable_population
        }

        st.session_state[
            "irb_completed"
        ] = True

        st.rerun()

    ethics_package = (
        st.session_state.get(
            "ethics_package"
        )
    )

    if ethics_package:

        st.subheader(
            "Generated Ethics Package"
        )

        st.markdown(
            ethics_package
        )

        st.download_button(
            "⬇️ Download IRB Package",
            data=ethics_package,
            file_name="IRB_package.md",
            use_container_width=True
        )

    if st.session_state.get(
        "irb_completed"
    ):

        st.success(
            "✅ Step 7 Completed"
        )
