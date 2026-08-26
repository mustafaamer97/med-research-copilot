import streamlit as st

from modules.docx_exporter import (
    export_to_docx
)
from modules.journal_recommender import (
    recommend_journals
)
from modules.manuscript_reviewer import (
    review_manuscript
)
from modules.manuscript_writer import (
    generate_manuscript
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

        st.divider()

        if st.button(
            "🔍 Review Manuscript",
            use_container_width=True
        ):

            with st.spinner(
                "Reviewing manuscript..."
            ):

                review = review_manuscript(
                    manuscript
                )

            st.session_state[
                "manuscript_review"
            ] = review

            st.rerun()

        st.download_button(
            "⬇️ Download Manuscript",
            data=manuscript,
            file_name="research_manuscript.md",
            use_container_width=True
        )

        if st.button(
            "📄 Export Manuscript to Word"
        ):

            output_file = export_to_docx(
                manuscript,
                "Research Manuscript",
                "research_manuscript.docx"
            )

            with open(
                output_file,
                "rb"
            ) as f:

                st.download_button(
                    "⬇️ Download DOCX",
                    data=f,
                    file_name="research_manuscript.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

    # ==================================
    # Display Review Report
    # ==================================

    review = st.session_state.get(
        "manuscript_review"
    )

    if review:

        st.subheader(
            "📋 Peer Review Report"
        )

        st.markdown(
            review
        )

        st.download_button(
            "⬇️ Download Review",
            data=review,
            file_name="peer_review_report.md",
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
