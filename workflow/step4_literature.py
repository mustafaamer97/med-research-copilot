import streamlit as st

from modules.multi_source_search import (
    search_all_sources
)

from modules.library import (
    save_paper
)

from modules.research_gap_detector import (
    detect_research_gaps
)

from modules.context_manager import (
    get_context,
    update_context
)


def render():

    st.header(
        "🔎 Literature Search & Evidence Review"
    )

    # 1) قراءة البيانات من Context وجلب البيانات الأساسية
    context_data = get_context()

    question_data = st.session_state.get(
        "research_question",
        context_data.get("research_question_data", {})
    )

    context = question_data.get(
        "context",
        st.session_state.get(
            "research_context",
            context_data
        )
    )
    disease = context.get(
        "disease",
        ""
    )
    location = context.get(
        "location",
        ""
    )
    study_period = context.get(
        "study_period",
        ""
    )
    study_design = context.get(
        "study_design",
        ""
    )
    research_goal = context.get(
        "research_goal",
        ""
    )

    pico_data = question_data.get(
        "pico",
        {}
    )

    population = pico_data.get(
        "population",
        context.get("population", "")
    )

    intervention = pico_data.get(
        "intervention",
        context.get("intervention", "")
    )

    comparison = pico_data.get(
        "comparison",
        context.get("comparison", "")
    )

    outcome = pico_data.get(
        "outcome",
        context.get("outcome", "")
    )

    if not question_data and not context:

        st.warning(
            "Please complete Step 3 first."
        )

        return

    # ==========================================
    # Research Question
    # ==========================================

    st.subheader(
        "Research Question"
    )

    st.info(
        question_data.get(
            "question",
            context.get("research_question", "No research question found.")
        )
    )

    # 3) إضافة بطاقة Context Summary
    with st.expander(
        "📋 Research Context",
        expanded=True
    ):
        st.write(
            f"**Disease:** {disease}"
        )
        st.write(
            f"**Population:** {population}"
        )
        st.write(
            f"**Outcome:** {outcome}"
        )
        st.write(
            f"**Location:** {location}"
        )
        st.write(
            f"**Period:** {study_period}"
        )
        st.write(
            f"**Design:** {study_design}"
        )
        st.write(
            f"**Goal:** {research_goal}"
        )

    # ==========================================
    # PICO Framework
    # ==========================================

    st.subheader(
        "PICO Framework"
    )

    st.json(
        pico_data if pico_data else {
            "population": population,
            "intervention": intervention,
            "comparison": comparison,
            "outcome": outcome
        }
    )

    # ==========================================
    # Search Queries
    # ==========================================

    default_query = (
        context.get("master_query")
        or context.get("pubmed_query")
        or question_data.get("master_query", "")
    )

    pubmed_query = question_data.get(
        "pubmed_query",
        ""
    )

    europe_pmc_query = question_data.get(
        "europe_pmc_query",
        ""
    )

    openalex_query = question_data.get(
        "openalex_query",
        ""
    )

    master_query = question_data.get(
        "master_query",
        default_query
    )

    # 2) استبدال بناء pico_query
    pico_query = " ".join(
        [
            x
            for x in [
                disease,
                population,
                intervention,
                comparison,
                outcome,
                location,
                study_period
            ]
            if x
        ]
    )

    st.markdown(
        "### 🔍 Search Strategy"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Master Query",
            "PubMed",
            "Europe PMC",
            "OpenAlex"
        ]
    )

    with tab1:

        query = st.text_area(
            "Search Query",
            value=master_query if master_query else default_query,
            height=120
        )

    with tab2:

        pubmed_query = st.text_area(
            "PubMed Query",
            value=pubmed_query,
            height=120
        )

    with tab3:

        europe_pmc_query = st.text_area(
            "Europe PMC Query",
            value=europe_pmc_query,
            height=120
        )

    with tab4:

        openalex_query = st.text_area(
            "OpenAlex Query",
            value=openalex_query,
            height=120
        )

    # ==========================================
    # Search Settings
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        number = st.selectbox(
            "Number of Papers",
            [5, 10, 20, 50, 100],
            index=2
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

    with col3:

        search_mode = st.selectbox(
            "Search Mode",
            [
                "Auto (Recommended)",
                "Manual Query"
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
            "Searching PubMed, Europe PMC and OpenAlex..."
        ):

            search_query = query

            # 4) تحسين Auto Search
            if search_mode == "Auto (Recommended)":

                search_query = " ".join(
                    [
                        disease,
                        population,
                        intervention,
                        comparison,
                        outcome,
                        location,
                        study_period
                    ]
                )

            papers = search_all_sources(
                search_query,
                max_results=number
            )

        st.session_state[
            "literature_search"
        ] = papers

        # 6) إضافة بيانات الأدلة للخطوة الخامسة
        st.session_state[
            "evidence_pool"
        ] = papers
        st.session_state[
            "selected_papers"
        ] = papers

        st.session_state[
            "retrieved_papers"
        ] = papers

        # 5) تخزين كل شيء للخطوة الخامسة
        st.session_state[
            "search_metadata"
        ] = {
            "query":
            search_query,
            "disease":
            disease,
            "population":
            population,
            "outcome":
            outcome,
            "location":
            location,
            "study_period":
            study_period,
            "study_design":
            study_design,
            "research_goal":
            research_goal,
            "pico":
            pico_data,
            "number_results":
            len(papers),
            "sources":
            [
                "PubMed",
                "Europe PMC",
                "OpenAlex"
            ]
        }

        update_context(
            evidence_count=len(papers),
            retrieved_papers=papers,
            literature_search_completed=True
        )

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
    # Research Gap Analysis
    # ==========================================

    analysis = st.session_state.get(
        "research_gap_analysis"
    )

    if not analysis:

        analysis = detect_research_gaps(
            papers
        )

        st.session_state[
            "research_gap_analysis"
        ] = analysis

        gap_results = analysis if isinstance(analysis, dict) else {}
        update_context(
            evidence_studies=gap_results.get(
                "total_papers",
                len(papers)
            ),
            research_gaps=gap_results.get(
                "research_gaps",
                []
            ),
            recent_evidence_percentage=gap_results.get(
                "recent_evidence_percentage",
                0
            )
        )

    st.subheader(
        "🎯 Research Gaps"
    )

    gaps_list = analysis.get("research_gaps", []) if isinstance(analysis, dict) else []
    for gap in gaps_list:

        st.warning(gap)

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
    # Source Filter
    # ==========================================

    source_filter = st.selectbox(
        "Source Filter",
        [
            "All",
            "PubMed",
            "Europe PMC",
            "OpenAlex"
        ]
    )

    if source_filter != "All":

        filtered_papers = [

            paper

            for paper in filtered_papers

            if paper.get(
                "source",
                ""
            ) == source_filter
        ]

    # ==========================================
    # Dashboard
    # ==========================================

    level1 = len(
        [
            p
            for p in papers
            if p.get(
                "evidence_level"
            ) == "Level 1"
        ]
    )

    level2 = len(
        [
            p
            for p in papers
            if p.get(
                "evidence_level"
            ) == "Level 2"
        ]
    )

    level3 = len(
        [
            p
            for p in papers
            if p.get(
                "evidence_level"
            ) == "Level 3"
        ]
    )

    level4 = len(
        [
            p
            for p in papers
            if p.get(
                "evidence_level"
            ) == "Level 4"
        ]
    )

    st.success(
        f"Found {len(filtered_papers)} papers after filtering"
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
    # Save All Papers
    # ==========================================

    if st.button(
        "💾 Save All Results",
        use_container_width=True
    ):

        saved_count = 0

        for paper in filtered_papers:

            result = save_paper(
                project_id=1,
                paper=paper
            )

            if result.get(
                "saved",
                False
            ):

                saved_count += 1

        st.success(
            f"{saved_count} papers saved successfully."
        )

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

        source = paper.get(
            "source",
            "Unknown"
        )

        citation_count = paper.get(
            "citation_count",
            0
        )

        with st.container():

            st.markdown("---")

            st.markdown(
                f"### 📄 {title}"
            )

            m1, m2, m3, m4 = st.columns(4)

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
                    "Source",
                    source
                )

            with m4:

                st.metric(
                    "Citations",
                    citation_count
                )

            st.caption(
                f"Journal: {journal}"
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
                        "🔗 Open Article",
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
