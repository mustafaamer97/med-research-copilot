import streamlit as st

from modules.manuscript_writer import (
    generate_manuscript
)

from modules.journal_recommender import (
    recommend_journals
)


def render():

    st.header(
        "📄 Manuscript Writer & Journal Finder"
    )

    literature = st.session_state.get(
        "literature_search",
        []
    )

    research_context = st.session_state.get(
        "research_context",
        {}
    )

    research_question = st.session_state.get(
        "research_question",
        {}
    )

    selected_idea = st.session_state.get(
        "selected_research_idea",
        {}
    )

    protocol = st.session_state.get(
        "research_protocol",
        ""
    )

    proposal = st.session_state.get(
        "research_proposal",
        ""
    )

    statistics_results = st.session_state.get(
        "statistics_results"
    )

    statistics_test = st.session_state.get(
        "statistics_test",
        ""
    )

    statistics_report = st.session_state.get(
        "statistics_report",
        ""
    )

    field = research_context.get(
        "field",
        ""
    )

    # ==================================
    # Statistics Status
    # ==================================

    st.subheader(
        "Statistical Analysis Status"
    )

    if statistics_results is not None:

        st.success(
            f"Statistics available ({statistics_test})"
        )

    else:

        st.warning(
            "No statistical analysis found. "
            "The manuscript can still be generated, "
            "but Results section will be limited."
        )

    # ==================================
    # Journal Recommendations
    # ==================================

    if literature:

        st.subheader(
            "🎯 Recommended Journals"
        )

        journals = recommend_journals(
            literature,
            field
        )

        for item in journals:

            st.info(
                f"""
Journal:
{item['journal']}

Supporting Papers:
{item['supporting_papers']}
"""
            )

    # ==================================
    # Generate Manuscript
    # ==================================

    if st.button(
        "📄 Generate Full Manuscript",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "Writing manuscript..."
        ):

            manuscript = generate_manuscript(
                research_context=research_context,
                research_question=research_question,
                selected_idea=selected_idea,
                protocol=protocol,
                proposal=proposal,
                literature=literature,
                statistics_results=statistics_report
            )

        st.session_state[
            "research_manuscript"
        ] = manuscript

        st.session_state[
            "manuscript_completed"
        ] = True

        st.rerun()

    # ==================================
    # Display Manuscript
    # ==================================

    manuscript = st.session_state.get(
        "research_manuscript"
    )

    if manuscript:

        st.subheader(
            "Generated Manuscript"
        )

        st.markdown(
            manuscript
        )

        st.download_button(
            "⬇️ Download Manuscript",
            data=manuscript,
            file_name="research_manuscript.md",
            use_container_width=True
        )

    # ==================================
    # Completion
    # ==================================

    if st.session_state.get(
        "manuscript_completed"
    ):

        st.success(
            "✅ Step 11 Completed"
        )
