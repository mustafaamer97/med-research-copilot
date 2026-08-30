import streamlit as st

from modules.context_manager import (
    get_context,
    update_context
)
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

    # 1. Fetch unified research context
    context = get_context()

    # Read needed components from context
    research_context = context
    research_question = context.get(
        "research_question",
        {}
    )
    selected_idea = context.get(
        "selected_research_idea",
        {}
    )
    literature = context.get(
        "literature_search",
        []
    )
    protocol = context.get(
        "research_protocol",
        ""
    )
    gap_analysis = context.get(
        "research_gap_analysis",
        {}
    )
    research_gaps = gap_analysis.get(
        "research_gaps",
        []
    )

    # Rich contextual methodology & ethics inputs
    sample_plan = context.get(
        "sample_size_plan",
        {}
    )
    data_collection_plan = context.get(
        "data_collection_plan",
        {}
    )
    ethics_summary = context.get(
        "ethics_summary",
        {}
    )

    # 2. Proposal Readiness Dashboard
    st.subheader(
        "Proposal Readiness"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Sample Size",
            "Ready"
            if context.get(
                "sample_size_completed"
            )
            else "Missing"
        )

    with c2:
        st.metric(
            "Ethics",
            "Ready"
            if context.get(
                "irb_completed"
            )
            else "Missing"
        )

    with c3:
        st.metric(
            "Data Collection",
            "Ready"
            if context.get(
                "data_collection_completed"
            )
            else "Missing"
        )

    # 3. Check for required completion before proceeding
    required_steps = [
        "sample_size_completed",
        "irb_completed",
        "data_collection_completed"
    ]

    missing = [
        step
        for step in required_steps
        if not context.get(step)
    ]

    if missing:
        st.warning(
            "Please complete previous steps first."
        )
        return

    # 4. Display Study Inputs Summary
    with st.expander(
        "📋 Proposal Inputs",
        expanded=True
    ):
        st.write(
            f"**Study Design:** {context.get('final_study_design', 'N/A')}"
        )
        st.write(
            f"**Sample Size:** {context.get('total_sample_size', 'N/A')}"
        )
        st.write(
            f"**Outcome:** {context.get('outcome', 'N/A')}"
        )

    # 5. Generate Proposal Action
    if st.button(
        "📑 Generate Proposal",
        use_container_width=True,
        type="primary"
    ):
        with st.spinner(
            "Building comprehensive research proposal..."
        ):
            proposal = generate_proposal(
                research_context=research_context,
                research_question=research_question,
                selected_idea=selected_idea,
                protocol=protocol,
                literature=literature,
                research_gaps=research_gaps,
                sample_size_plan=sample_plan,
                data_collection_plan=data_collection_plan,
                ethics_summary=ethics_summary
            )

        update_context(
            research_proposal=proposal,
            proposal_completed=True
        )

        st.rerun()

    # 6. Display and Export Proposal
    proposal = context.get(
        "research_proposal"
    )

    if proposal:
        st.markdown(
            proposal
        )

        st.download_button(
            "⬇️ Download Proposal (.md)",
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

    if context.get(
        "proposal_completed"
    ):
        st.success(
            "✅ Step 10 Completed"
        )
