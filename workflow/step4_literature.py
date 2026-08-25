import streamlit as st

from modules.pubmed import search_pubmed
from modules.library import save_paper


def render():

    st.header(
        "🔎 Literature Search & Evidence Review"
    )

    st.info(
        "Workflow validation is temporarily disabled during development."
    )

    # ==========================================
    # Research Question
    # ==========================================

    question_data = st.session_state.get(
        "research_question",
        {}
    )

    if question_data:

        st.subheader(
            "Research Question"
        )

        st.info(
            question_data.get(
                "question",
                "No research question found."
            )
        )

    # ==========================================
    # Search Query
    # ==========================================

    default_keywords = question_data.get(
        "keywords",
        ""
    )

    st.markdown(
        "### 🔍 Search Strategy"
    )

    query = st.text_area(
        "PubMed Search Query",
        value=default_keywords,
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:

        number = st.selectbox(
            "Number of Papers",
            [5, 10, 20, 50],
            index=1
        )

    with col2:

        evidence_filter = st.selectbox(
            "Evidence Filter",
            [
                "All",
                "Level 1",
                "Level 2",
                "Level 3",
                "Level 4"
            ]
        )

    # ==========================================
    # Search Button
    # ==========================================

    if st.button(
        "🔎 Search Literature",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "Searching PubMed..."
        ):

            papers = search_pubmed(
                query,
                number
            )

        st.session_state[
            "literature_search"
        ] = papers

        st.session_state[
            "literature_completed"
        ] = len(papers) > 0

        st.rerun()

    # ==========================================
    # Results
    # ==========================================

    papers = st.session_state.get(
        "literature_search",
        []
    )

    if not papers:
        return

    # ==========================================
    # Filtering
    # ==========================================

    filtered_papers = papers

    if evidence_filter != "All":

        filtered_papers = [

            paper
            for paper in papers

            if paper.get(
                "evidence_level"
            ) == evidence_filter
        ]

    # ==========================================
    # Dashboard
    # ==========================================

    level1 = len([
        p for p in papers
        if p.get("evidence_level") == "Level 1"
    ])

    level2 = len([
        p for p in papers
        if p.get("evidence_level") == "Level 2"
    ])

    level3 = len([
        p for p in papers
        if p.get("evidence_level") == "Level 3"
    ])

    level4 = len([
        p for p in papers
        if p.get("evidence_level") == "Level 4"
    ])

    st.success(
        f"Found {len(filtered_papers)} papers"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total",
        len(papers)
    )

    c2.metric(
        "Level 1",
        level1
    )

    c3.metric(
        "Level 2",
        level2
    )

    c4.metric(
        "Level 3",
        level3
    )

    c5.metric(
        "Level 4",
        level4
    )

    st.divider()

    # ==========================================
    # Papers
    # ==========================================

    for idx, paper in enumerate(
        filtered_papers
    ):

        title = paper.get(
            "title",
            "No Title"
        )

        journal = paper.get(
            "journal",
            "Unknown Journal"
        )

        year = paper.get(
            "year",
            "N/A"
        )

        evidence = paper.get(
            "evidence_level",
            "Unknown"
        )

        doi = paper.get(
            "doi",
            ""
        )

        abstract = paper.get(
            "abstract",
            "No abstract available."
        )

        authors = paper.get(
            "authors",
            ""
        )

        url = paper.get(
            "url",
            ""
        )

        with st.container():

            st.markdown("---")

            st.markdown(
                f"### 📄 {title}"
            )

            m1, m2, m3 = st.columns(3)

            with m1:

                st.metric(
                    "Year",
                    year
                )

            with m2:

                st.metric(
                    "Evidence",
                    evidence
                )

            with m3:

                st.metric(
                    "Journal",
                    journal[:20]
                )

            if authors:

                st.caption(
                    f"Authors: {authors}"
                )

            if doi:

                st.caption(
                    f"DOI: {doi}"
                )

            with st.expander(
                "📖 Abstract"
            ):

                st.write(
                    abstract
                )

            btn1, btn2 = st.columns(2)

            with btn1:

                if url:

                    st.link_button(
                        "🔗 Open PubMed",
                        url
                    )

            with btn2:

                if st.button(
                    "💾 Save Paper",
                    key=f"save_{idx}"
                ):

                    result = save_paper(
                        project_id=1,
                        paper=paper
                    )

                    if result["saved"]:

                        st.success(
                            result["message"]
                        )

                    else:

                        st.warning(
                            result["message"]
                        )

    # ==========================================
    # Step Completed
    # ==========================================

    if st.session_state.get(
        "literature_completed"
    ):

        st.success(
            "✅ Step 4 Completed"
        )
