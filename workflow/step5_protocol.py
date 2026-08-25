import streamlit as st

from modules.protocol_builder import (
    generate_protocol
)

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


def render():

    st.header(
        "📋 Research Protocol Builder"
    )

    st.info(
        "Generate a complete research protocol from your selected idea."
    )

    # ==================================
    # Load Idea Automatically
    # ==================================

    selected_idea = st.session_state.get(
        "selected_research_idea",
        {}
    )

    default_idea = selected_idea.get(
        "description",
        ""
    )

    if selected_idea:

        st.subheader(
            "Selected Research Idea"
        )

        st.info(
            f"""
Title:
{selected_idea.get('title', '')}

Description:
{selected_idea.get('description', '')}
"""
        )

    # ==================================
    # Protocol Inputs
    # ==================================

    idea = st.text_area(
        "Research Idea",
        value=default_idea,
        height=180
    )

    study_type = st.selectbox(
        "Study Design",
        STUDY_DESIGNS
    )

    # ==================================
    # Generate Protocol
    # ==================================

    if st.button(
        "📋 Generate Protocol",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "Building protocol..."
        ):

            protocol = generate_protocol(
                idea,
                study_type
            )

        st.session_state[
            "research_protocol"
        ] = protocol

        st.session_state[
            "protocol_completed"
        ] = True

        st.rerun()

    # ==================================
    # Display Protocol
    # ==================================

    protocol = st.session_state.get(
        "research_protocol"
    )

    if protocol:

        st.subheader(
            "Generated Protocol"
        )

        st.markdown(
            protocol
        )

        st.download_button(
            "⬇️ Download Protocol",
            data=protocol,
            file_name="research_protocol.md",
            use_container_width=True
        )

    # ==================================
    # Completion Status
    # ==================================

    if st.session_state.get(
        "protocol_completed"
    ):

        st.success(
            "✅ Step 5 Completed"
        )
