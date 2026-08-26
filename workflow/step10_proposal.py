import streamlit as st

from modules.docx_exporter import (
    export_to_docx
)
from modules.proposal_builder import (
    generate_proposal
)


def render():

    st.header(
        "📑 Research Proposal Builder"
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

    literature = st.session_state.get(
        "literature_search",
        []
    )

    protocol = st.session_state.get(
        "research_protocol",
        ""
    )

    gap_analysis = st.session_state.get(
        "research_gap_analysis",
        {}
    )

    research_gaps = gap_analysis.get(
        "research_gaps",
        []
    )

    if st.button(
        "📑 Generate Proposal",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "Building proposal..."
        ):

            proposal = generate_proposal(
                research_context=research_context,
                research_question=research_question,
                selected_idea=selected_idea,
                protocol=protocol,
                literature=literature,
                research_gaps=research_gaps
            )

        st.session_state[
            "research_proposal"
        ] = proposal

        st.session_state[
            "proposal_completed"
        ] = True

        st.rerun()

    proposal = st.session_state.get(
        "research_proposal"
    )

    if proposal:

        st.markdown(
            proposal
        )

        st.download_button(
            "⬇️ Download Proposal",
            data=proposal,
            file_name="research_proposal.md",
            use_container_width=True
        )

        docx_file = export_to_docx(
            proposal,
            "Research Proposal",
            "research_proposal.docx"
        )

        with open(
            docx_file,
            "rb"
        ) as file:

            st.download_button(
                "⬇️ Download Proposal (.docx)",
                data=file,
                file_name="research_proposal.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

    if st.session_state.get(
        "proposal_completed"
    ):

        st.success(
            "✅ Step 10 Completed"
        )
