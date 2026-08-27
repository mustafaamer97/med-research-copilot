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


def build_smart_search_query(question_data):
    """
    Builds structured smart search queries (PICO, Broad, and Evidence-based)
    to optimize search recall and precision across literature databases.
    """
    pico_data = question_data.get("pico", {})

    population = pico_data.get("population", "").strip()
    intervention = pico_data.get("intervention", "").strip()
    comparison = pico_data.get("comparison", "").strip()
    outcome = pico_data.get("outcome", "").strip()

    # 1. PICO Query
    pico_terms = [x for x in [population, intervention, comparison, outcome] if x]
    pico_query = " ".join(pico_terms)

    # 2. Broad Query (Population + Intervention)
    broad_terms = [x for x in [population, intervention] if x]
    broad_query = " ".join(broad_terms)

    # 3. Evidence Query (Appends study design filters)
    evidence_filters = "(systematic review OR meta-analysis OR randomized controlled trial OR cohort study)"
    
    if broad_query:
        evidence_query = f"{broad_query} {evidence_filters}"
    elif pico_query:
        evidence_query = f"{pico_query} {evidence_filters}"
    else:
        evidence_query = evidence_filters

    master_query = question_data.get("master_query", "").strip()

    # Smart fallback / auto query combination
    if master_query and pico_query:
        smart_query = f"{master_query} {pico_query} {evidence_filters}"
    elif master_query:
        smart_query = f"{master_query} {evidence_filters}"
    elif pico_query:
        smart_query = evidence_query
    else:
        smart_query = ""

    return {
        "pico_query": pico_query,
        "broad_query": broad_query,
        "evidence_query": evidence_query,
        "smart_query": smart_query
    }


def render():

    st.header(
        "🔎 Literature Search & Evidence Review"
    )

    question_data = st.session_state.get(
        "research_question",
        {}
    )

    if not question_data:

        st.warning(
            "Please complete Step 3 first."
        )

        return

    # Extract PICO data
    pico_data = question_data.get(
        "pico",
        {}
    )

    population = pico_data.get("population", "")
    intervention = pico_data.get("intervention", "")
    comparison = pico_data.get("comparison", "")
    outcome = pico_data.get("outcome", "")

    # Build Smart Search Queries
    smart_queries = build_smart_search_query(question_data)

    # ==========================================
    # Research Question
    # ==========================================

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
    # PICO Framework
    # ==========================================

    st.subheader(
        "PICO Framework"
    )

    st.json(
        pico_data
    )

    # ==========================================
    # Search Queries
    # ==========================================

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
        ""
    )

    st.markdown(
        "### 🔍 Search Strategy"
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "PubMed",
            "Europe PMC",
            "OpenAlex",
            "Master Query",
            "Smart Query"
        ]
    )

    with tab1:

        pubmed_query = st.text_area(
            "PubMed Query",
            value=pubmed_query,
            height=120
        )

    with tab2:

        europe_pmc_query = st.text_area(
            "Europe PMC Query",
            value=europe_pmc_query,
            height=120
        )

    with tab3:

        openalex_query = st.text_area(
            "OpenAlex Query",
            value=openalex_query,
            height=120
        )

    with tab4:

        master_query = st.text_area(
            "Master Query",
            value=master_query,
            height=120
        )

    with tab5:

        smart_query_input = st.text_area(
            "Smart Combined Query",
            value=smart_queries.get("smart_query", ""),
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

            if search_mode == "Auto (Recommended)":
                search_query = smart_queries.get("smart_query") or master_query
            else:
                search_query = master_query

            papers = search_all_sources(
                search_query,
                max_results=number
            )

        # Prepare screening articles with standard default keys for Step 5
        screening_articles = []
        for p in papers:
            article = {
                "title": p.get("title", ""),
                "abstract": p.get("abstract", "No abstract available."),
                "pmid": p.get("pmid", ""),
                "doi": p.get("doi", ""),
                "authors": p.get("authors", ""),
                "year": p.get("year", "N/A"),
                "source": p.get("source", "Unknown"),
                "decision": "",
                "exclusion_reason": ""
            }
            screening_articles.append(article)

        st.session_state["literature_search"] = papers
        st.session_state["screening_articles"] = screening_articles

        st.session_state["search_metadata"] = {
            "query": search_query,
            "pico": pico_data,
            "number_results": len(papers),
            "sources": ["PubMed", "Europe PMC", "OpenAlex"]
        }

        st.session_state["literature_completed"] = len(papers) > 0

        # Clear cached gap analysis for new search
        if "research_gap_analysis" in st.session_state:
            del st.session_state["research_gap_analysis"]

        st.rerun()

    # ==========================================
    # Results Check
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

    st.subheader(
        "🎯 Research Gaps Analysis"
    )

    # Structured Gap Categories Display
    gap_categories = [
        ("Missing Evidence", analysis.get("missing_evidence", [])),
        ("Lack of RCTs", analysis.get("lack_of_rcts", [])),
        ("Lack of Meta-Analysis", analysis.get("lack_of_meta_analysis", [])),
        ("Population Gaps", analysis.get("population_gaps", [])),
        ("Geographic Gaps", analysis.get("geographic_gaps", []))
    ]

    has_structured_gaps = any(len(items) > 0 for _, items in gap_categories)

    if has_structured_gaps:

        for cat_name, gap_items in gap_categories:

            if gap_items:

                st.markdown(f"**{cat_name}:**")

                for item in gap_items:

                    st.warning(item)

    else:

        for gap in analysis.get(
            "research_gaps",
            []
        ):

            st.warning(gap)

    # ==========================================
    # Filtering & Sorting Controls
    # ==========================================

    col_filt1, col_filt2, col_filt3 = st.columns(3)

    with col_filt1:

        evidence_filter = st.selectbox(
            "Filter by Evidence",
            [
                "All",
                "Level 1",
                "Level 2",
                "Level 3",
                "Level 4"
            ],
            key="filter_evidence_dropdown"
        )

    with col_filt2:

        source_filter = st.selectbox(
            "Filter by Source",
            [
                "All",
                "PubMed",
                "Europe PMC",
                "OpenAlex"
            ],
            key="filter_source_dropdown"
        )

    with col_filt3:

        sort_option = st.selectbox(
            "Sort Papers",
            [
                "Evidence Score",
                "Year",
                "Citations",
                "Source"
            ]
        )

    filtered_papers = papers

    if evidence_filter != "All":

        filtered_papers = [
            paper for paper in filtered_papers
            if paper.get("evidence_level") == evidence_filter
        ]

    if source_filter != "All":

        filtered_papers = [
            paper for paper in filtered_papers
            if paper.get("source", "") == source_filter
        ]

    # Apply Sorting
    if sort_option == "Evidence Score":
        filtered_papers = sorted(
            filtered_papers,
            key=lambda x: x.get("evidence_score", 0),
            reverse=True
        )
    elif sort_option == "Year":
        filtered_papers = sorted(
            filtered_papers,
            key=lambda x: str(x.get("year", "0")),
            reverse=True
        )
    elif sort_option == "Citations":
        filtered_papers = sorted(
            filtered_papers,
            key=lambda x: x.get("citation_count", 0),
            reverse=True
        )
    elif sort_option == "Source":
        filtered_papers = sorted(
            filtered_papers,
            key=lambda x: x.get("source", "")
        )

    # ==========================================
    # Evidence Dashboard
    # ==========================================

    level1 = len([p for p in papers if p.get("evidence_level") == "Level 1"])
    level2 = len([p for p in papers if p.get("evidence_level") == "Level 2"])
    level3 = len([p for p in papers if p.get("evidence_level") == "Level 3"])
    
    scores = [p.get("evidence_score", 0) for p in papers if p.get("evidence_score") is not None]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    open_access_count = len([p for p in papers if p.get("is_open_access") is True])

    st.success(
        f"Found {len(filtered_papers)} papers after filtering"
    )

    d1, d2, d3, d4, d5, d6 = st.columns(6)

    d1.metric("Total Papers", len(papers))
    d2.metric("Level 1", level1)
    d3.metric("Level 2", level2)
    d4.metric("Level 3", level3)
    d5.metric("Avg Score", avg_score)
    d6.metric("Open Access", open_access_count)

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

            if result.get("saved", False):

                saved_count += 1

        st.success(
            f"{saved_count} papers saved successfully."
        )

    # ==========================================
    # Display Papers as Cards
    # ==========================================

    for idx, paper in enumerate(filtered_papers):

        title = paper.get("title", "No Title")
        journal = paper.get("journal", "Unknown Journal")
        year = paper.get("year", "N/A")
        evidence = paper.get("evidence_level", "Unknown")
        evidence_score = paper.get("evidence_score", "N/A")
        doi = paper.get("doi", "")
        abstract = paper.get("abstract", "No abstract available.")
        authors = paper.get("authors", "")
        url = paper.get("url", "")
        source = paper.get("source", "Unknown")
        citation_count = paper.get("citation_count", 0)

        with st.container():

            st.markdown("---")

            st.markdown(f"### 📄 {title}")

            m1, m2, m3, m4, m5 = st.columns(5)

            with m1:
                st.metric("Year", year)

            with m2:
                st.metric("Evidence Level", evidence)

            with m3:
                st.metric("Score", evidence_score)

            with m4:
                st.metric("Source", source)

            with m5:
                st.metric("Citations", citation_count)

            st.caption(f"**Journal:** {journal}")

            if authors:
                st.caption(f"**Authors:** {authors}")

            if doi:
                st.caption(f"**DOI:** {doi}")

            with st.expander("📖 Abstract"):
                st.write(abstract)

            btn1, btn2 = st.columns(2)

            with btn1:
                if url:
                    st.link_button(
                        "🔗 Open Article",
                        url,
                        use_container_width=True
                    )

            with btn2:
                if st.button(
                    "💾 Save Paper",
                    key=f"save_{idx}",
                    use_container_width=True
                ):
                    result = save_paper(
                        project_id=1,
                        paper=paper
                    )

                    if result.get("saved"):
                        st.success(result.get("message", "Saved!"))
                    else:
                        st.warning(result.get("message", "Already saved or error."))

    # ==========================================
    # Step Completion & Transition to Step 5
    # ==========================================

    if len(papers) > 0:

        st.markdown("---")

        st.success("✅ Step 4 Completed")

        if st.button(
            "➡️ Proceed to Article Screening (Step 5)",
            type="primary",
            use_container_width=True
        ):
            st.session_state["current_step"] = 5
            st.rerun()
