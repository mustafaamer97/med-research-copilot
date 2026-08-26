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
    # Protocol Version
    # ==================================

    st.caption(
        f"Protocol Version: v{len(st.session_state.get('protocol_history', [])) + 1}"
    )

    # ==================================
    # Tabs
    # ==================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Context",
            "Idea",
            "Evidence",
            "Protocol Builder"
        ]
    )

    # ==================================
    # Context Tab
    # ==================================

    with tab1:

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
    # Idea Tab
    # ==================================

    with tab2:

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
    # Evidence Tab
    # ==================================

    with tab3:

        st.subheader(
            "Evidence Summary"
        )

        st.metric(
            "Retrieved Papers",
            len(literature)
        )

        st.metric(
            "Evidence Used",
            len(literature)
        )

        if literature:

            for paper in literature[:10]:

                st.caption(
                    f"""
{paper.get('year','')} |
{paper.get('evidence_level','Unknown')} |
{paper.get('source','Unknown')}

{paper.get('title','')}
"""
                )

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

            if gap_analysis.get(
                "research_gaps"
            ):

                with st.expander(
                    "Research Gaps Used in Protocol"
                ):

                    for gap in gap_analysis[
                        "research_gaps"
                    ]:

                        st.write(
                            f"• {gap}"
                        )

    # ==================================
    # Protocol Builder Tab
    # ==================================

    with tab4:

        default_idea = selected_idea.get(
            "description",
            ""
        )

        idea = st.text_area(
            "Research Idea",
            value=default_idea,
            height=180
        )

        default_study_design = (
            research_context.get(
                "study_design",
                STUDY_DESIGNS[0]
            )
        )

        study_index = 0

        if default_study_design in STUDY_DESIGNS:

            study_index = STUDY_DESIGNS.index(
                default_study_design
            )

        study_type = st.selectbox(
            "Study Design",
            STUDY_DESIGNS,
            index=study_index
        )

        col1, col2 = st.columns(2)

        with col1:

            generate_btn = st.button(
                "📋 Generate Protocol",
                use_container_width=True,
                type="primary"
            )

        with col2:

            regenerate_btn = st.button(
                "🔄 Regenerate Protocol",
                use_container_width=True
            )

        if generate_btn or regenerate_btn:

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

            if (
                "protocol_history"
                not in st.session_state
            ):

                st.session_state[
                    "protocol_history"
                ] = []

            st.session_state[
                "protocol_history"
            ].append(protocol)

            st.session_state[
                "research_protocol"
            ] = protocol

            st.session_state[
                "protocol_completed"
            ] = True

            st.rerun()

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

            with st.expander(
                "Protocol Quality Checklist",
                expanded=True
            ):

                st.checkbox(
                    "Research Question Defined",
                    value=bool(
                        research_question
                    ),
                    disabled=True
                )

                st.checkbox(
                    "Literature Search Completed",
                    value=len(
                        literature
                    ) > 0,
                    disabled=True
                )

                st.checkbox(
                    "Research Gaps Identified",
                    value=bool(
                        gap_analysis
                    ),
                    disabled=True
                )

                st.checkbox(
                    "Study Design Selected",
                    value=bool(
                        study_type
                    ),
                    disabled=True
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
