def build_protocol_context():

    import streamlit as st

    context = st.session_state.get(
        "research_context",
        {}
    )

    idea = st.session_state.get(
        "selected_research_idea",
        {}
    )

    question = st.session_state.get(
        "research_question",
        {}
    )

    papers = st.session_state.get(
        "literature_search",
        []
    )

    top_papers = papers[:5]

    evidence_summary = []

    for paper in top_papers:

        evidence_summary.append(
            f"""
Title: {paper.get('title','')}

Evidence: {paper.get('evidence_level','')}

Year: {paper.get('year','')}
"""
        )

    return {
        "context": context,
        "idea": idea,
        "question": question,
        "evidence": evidence_summary
    }
