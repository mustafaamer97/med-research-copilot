import streamlit as st

from modules.context_manager import (
    get_context,
    update_context
)
from modules.ethics_builder import (
    generate_ethics_package
)


def render():

    st.header(
        "🛡️ Ethics & IRB Preparation"
    )

    # جلب السياق الكامل من Context Manager
    context = get_context()

    # ==================================
    # Research Summary
    # ==================================

    with st.expander(
        "📋 Research Summary",
        expanded=True
    ):
        st.write(
            f"**Disease:** {context.get('disease', '')}"
        )
        st.write(
            f"**Population:** {context.get('population', '')}"
        )
        st.write(
            f"**Outcome:** {context.get('outcome', '')}"
        )
        st.write(
            f"**Sample Size:** {context.get('total_sample_size', '')}"
        )
        st.write(
            f"**Study Design:** {context.get('final_study_design') or context.get('study_design') or 'Clinical Study'}"
        )

    research_question = (
        context.get(
            "research_question_data",
            {}
        )
    )

    protocol = context.get(
        "research_protocol",
        ""
    )

    study_type = (
        context.get(
            "final_study_design"
        )
        or context.get(
            "study_design"
        )
        or "Clinical Study"
    )

    # ==================================
    # Study Summary Dashboard
    # ==================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            f"**Study Type:** {study_type}"
        )

    with c2:

        st.metric(
            "Research Question",
            "Available"
            if research_question
            else "Missing"
        )

    with c3:

        st.metric(
            "Protocol",
            "Available"
            if protocol
            else "Missing"
        )

    # ==================================
    # Risk Recommendation
    # ==================================

    recommended_risk = "Moderate Risk"

    if any(
        x in study_type.lower()
        for x in [
            "cross",
            "survey",
            "case report",
            "case series"
        ]
    ):

        recommended_risk = "Minimal Risk"

    elif any(
        x in study_type.lower()
        for x in [
            "cohort",
            "case-control"
        ]
    ):

        recommended_risk = "Moderate Risk"

    elif any(
        x in study_type.lower()
        for x in [
            "trial",
            "randomized",
            "clinical"
        ]
    ):

        recommended_risk = "High Risk"

    st.info(
        f"Recommended Risk Level: {recommended_risk}"
    )

    st.subheader(
        "IRB Settings"
    )

    # ==================================
    # IRB Documents Checklist
    # ==================================

    st.subheader(
        "Required IRB Documents"
    )

    st.checkbox(
        "Research Protocol",
        value=bool(protocol),
        disabled=True
    )

    st.checkbox(
        "Research Question",
        value=bool(research_question),
        disabled=True
    )

    consent_form_ready = st.checkbox(
        "Consent Form Prepared"
    )

    data_sheet_ready = st.checkbox(
        "Data Collection Sheet Prepared"
    )

    st.divider()

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

    # ==================================
    # IRB Readiness Score
    # ==================================

    score = 0

    if protocol:
        score += 40

    if research_question:
        score += 20

    if consent_form_ready:
        score += 20

    if data_sheet_ready:
        score += 10

    if not vulnerable_population:
        score += 10

    st.subheader(
        "IRB Readiness"
    )

    st.progress(
        score / 100
    )

    st.caption(
        f"IRB Readiness Score: {score}%"
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

            ethics_package = generate_ethics_package(
                research_question=
                research_question.get(
                    "question",
                    ""
                ),
                study_type=study_type,
                risk_level=study_risk,
                informed_consent=informed_consent,
                vulnerable_population=vulnerable_population,
                protocol=protocol,
                sample_size_plan=context.get(
                    "sample_size_plan",
                    {}
                ),
                research_context=context,
                research_gaps=context.get(
                    "research_gaps",
                    []
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
            vulnerable_population,

            "recommended_risk":
            recommended_risk,

            "irb_readiness":
            score
        }

        st.session_state[
            "ethics_summary"
        ] = {

            "study_type":
            study_type,

            "risk":
            study_risk,

            "recommended_risk":
            recommended_risk,

            "consent":
            informed_consent,

            "vulnerable_population":
            vulnerable_population,

            "irb_readiness":
            score
        }

        st.session_state[
            "irb_completed"
        ] = True

        # حفظ البيانات في الـ Context Manager
        update_context(
            ethics_package=ethics_package,
            ethics_summary={
                "study_type": study_type,
                "risk": study_risk,
                "recommended_risk": recommended_risk,
                "consent": informed_consent,
                "vulnerable_population": vulnerable_population,
                "irb_readiness": score
            },
            irb_completed=True,
            irb_readiness=score,
            risk_level=study_risk
        )

        st.rerun()

    ethics_package = (
        st.session_state.get(
            "ethics_package"
        )
        or context.get("ethics_package")
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

    if (
        context.get("irb_completed")
        or st.session_state.get(
            "irb_completed"
        )
    ):

        st.success(
            "✅ Step 7 Completed"
        )
