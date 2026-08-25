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

    # ==================================
    # Load Previous Steps
    # ==================================

    research_context = st.session_state.get(
        "research_context",
        {}
    )

    selected_idea = st.session_state.get(
        "selected_research_idea",
        {}
    )

    research_question = st.session_state.get(
        "research_question",
        {}
    )

    literature = st.session_state.get(
        "literature_search",
        []
    )

    gap_analysis = st.session_state.get(
        "research_gap_analysis",
        {}
    )

    # ==================================
    # Context Summary
    # ==================================

    st.subheader(
        "Research Context"
    )

    if research_context:

        st.info(
            f"""
Field: {research_context.get('field','')}

Population: {research_context.get('population','')}

Study Design: {research_context.get('study_design','')}

Data Source: {research_context.get('data_source','')}
"""
        )

    # ==================================
    # Research Idea
    # ==================================

    if selected_idea:

        st.subheader(
            "Research Idea"
        )

        st.info(
            f"""
Title:
{selected_idea.get('title','')}

Description:
{selected_idea.get('description','')}
"""
        )

    # ==================================
    # Research Question
    # ==================================

    if research_question:

        st.subheader(
            "Research Question"
        )

        st.success(
            research_question.get(
                "question",
                ""
            )
        )

    # ==================================
    # Evidence Summary
    # ==================================

    if literature:

        st.subheader(
            "Evidence Summary"
        )

        st.metric(
            "Retrieved Papers",
            len(literature)
        )

        for paper in literature[:5]:

            st.caption(
                f"""
{paper.get('year','')} |
{paper.get('evidence_level','Unknown')}

{paper.get('title','')}
"""
            )

    # ==================================
    # Research Gap Summary
    # ==================================

    if gap_analysis:

        st.subheader(
            "Research Gap Analysis"
        )

        top_keywords = gap_analysis.get(
            "top_keywords",
            []
        )

        if top_keywords:

            st.write(
                "Most Common Literature Keywords"
            )

            st.write(
                ", ".join(
                    [
                        item[0]
                        for item in top_keywords[:10]
                    ]
                )
            )

    # ==================================
    # Protocol Inputs
    # ==================================

    default_idea = selected_idea.get(
        "description",
        ""
    )

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
                research_idea=idea,
                study_type=study_type,
                research_context=research_context,
                research_question=research_question,
                research_gaps=gap_analysis.get(
                    "research_gaps",
                    []
                ),
                keywords=gap_analysis.get(
                    "top_keywords",
                    []
                )
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
    # Completion
    # ==================================

    if st.session_state.get(
        "protocol_completed"
    ):

        st.success(
            "✅ Step 5 Completed"
        )
