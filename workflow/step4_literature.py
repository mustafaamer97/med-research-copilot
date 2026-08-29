import streamlit as st

from modules.multi_source_search import search_all_sources
from modules.library import save_paper
from modules.research_gap_detector import detect_research_gaps
from modules.context_manager import get_context, update_context
from components.paper_card import render_paper_card


def render():
    st.header("🔎 Literature Search & Evidence Review")

    # 1) قراءة Context الموحد وتجميع البيانات
    context = get_context()

    question_data = st.session_state.get(
        "research_question",
        context.get("research_question_data", {})
    )

    disease = context.get("disease", "")
    location = context.get("location", "")
    study_period = context.get("study_period", "")
    study_design = context.get("study_design", "")
    research_goal = context.get("research_goal", "")

    pico_data = question_data.get("pico", {}) if isinstance(question_data, dict) else {}

    population = context.get("population") or pico_data.get("population", "")
    intervention = context.get("intervention") or pico_data.get("intervention", "")
    comparison = context.get("comparison") or pico_data.get("comparison", "")
    outcome = context.get("outcome") or pico_data.get("outcome", "")

    if not context and not question_data:
        st.warning("Please complete Step 3 first.")
        return

    # ==========================================
    # Research Question
    # ==========================================

    st.subheader("Research Question")
    st.info(
        context.get("research_question")
        or question_data.get("question", "No research question found.")
    )

    # Context Summary
    with st.expander("📋 Research Context", expanded=True):
        st.write(f"**Disease:** {disease}")
        st.write(f"**Population:** {population}")
        st.write(f"**Outcome:** {outcome}")
        st.write(f"**Location:** {location}")
        st.write(f"**Period:** {study_period}")
        st.write(f"**Design:** {study_design}")
        st.write(f"**Goal:** {research_goal}")

    # ==========================================
    # PICO Framework
    # ==========================================

    st.subheader("PICO Framework")
    st.json(
        pico_data if pico_data else {
            "population": population,
            "intervention": intervention,
            "comparison": comparison,
            "outcome": outcome
        }
    )

    # ==========================================
    # Search Strategy
    # ==========================================

    st.markdown("### 🔍 Search Strategy")

    master_query = question_data.get("master_query", "") if isinstance(question_data, dict) else ""
    if not master_query:
        master_query = context.get("master_query", "")

    query = st.text_area(
        "Master Query",
        value=master_query,
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
            ["All", "Level 1", "Level 2", "Level 3", "Level 4"]
        )

    with col3:
        search_mode = st.selectbox(
            "Search Mode",
            ["Auto (Recommended)", "Manual Query"]
        )

    # ==========================================
    # Search Button
    # ==========================================

    if st.button("🔎 Search Literature", use_container_width=True, type="primary"):
        with st.spinner("Searching PubMed, Europe PMC and OpenAlex..."):
            search_query = query

            # 2) تنظيف Auto Search ومنع المسافات الفارغة
            if search_mode == "Auto (Recommended)":
                search_query = " ".join(
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

            # 4) إضافة حماية من البحث الفارغ
            if not search_query.strip():
                st.warning("Search query is empty.")
                st.stop()

            papers = search_all_sources(
                search_query,
                max_results=number
            )

        st.session_state["literature_search"] = papers
        st.session_state["evidence_pool"] = papers
        st.session_state["selected_papers"] = papers
        
        # 5) تجهيز البيانات لـ Step 5 مباشرة
        st.session_state["papers_for_extraction"] = papers

        st.session_state["search_metadata"] = {
            "query": search_query,
            "disease": disease,
            "population": population,
            "outcome": outcome,
            "location": location,
            "study_period": study_period,
            "study_design": study_design,
            "research_goal": research_goal,
            "pico": pico_data,
            "number_results": len(papers),
            "sources": ["PubMed", "Europe PMC", "OpenAlex"]
        }

        # 3) حفظ query المعتمد في Context
        update_context(
            master_query=search_query,
            evidence_count=len(papers),
            retrieved_papers=papers,
            literature_search_completed=True
        )

        st.session_state["literature_completed"] = len(papers) > 0
        st.rerun()

    # ==========================================
    # Results
    # ==========================================

    papers = st.session_state.get("literature_search", [])
    if not papers:
        return

    # ==========================================
    # Research Gap Analysis
    # ==========================================

    # 1) منع إعادة حساب Research Gaps عند تغيير البحث عبر مفتاح ديناميكي
    current_query = st.session_state.get(
        "search_metadata",
        {}
    ).get(
        "query",
        ""
    )
    analysis_key = f"gap_{current_query}"
    analysis = st.session_state.get(analysis_key)

    if not analysis:
        analysis = detect_research_gaps(papers)
        st.session_state[analysis_key] = analysis

        gap_results = analysis if isinstance(analysis, dict) else {}
        update_context(
            evidence_studies=gap_results.get("total_papers", len(papers)),
            research_gaps=gap_results.get("research_gaps", []),
            recent_evidence_percentage=gap_results.get("recent_evidence_percentage", 0)
        )

    st.subheader("🎯 Research Gaps")
    gaps_list = analysis.get("research_gaps", []) if isinstance(analysis, dict) else []
    for gap in gaps_list:
        st.warning(gap)

    # ==========================================
    # Filtering
    # ==========================================

    filtered_papers = papers

    if evidence_filter != "All":
        filtered_papers = [
            paper for paper in papers
            if paper.get("evidence_level") == evidence_filter
        ]

    source_filter = st.selectbox(
        "Source Filter",
        ["All", "PubMed", "Europe PMC", "OpenAlex"]
    )

    if source_filter != "All":
        filtered_papers = [
            paper for paper in filtered_papers
            if paper.get("source", "") == source_filter
        ]

    # ==========================================
    # Dashboard
    # ==========================================

    levels = {}
    for paper in papers:
        level = paper.get("evidence_level", "Unknown")
        levels[level] = levels.get(level, 0) + 1

    st.success(f"Found {len(filtered_papers)} papers after filtering")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", len(papers))
    c2.metric("Level 1", levels.get("Level 1", 0))
    c3.metric("Level 2", levels.get("Level 2", 0))
    c4.metric("Level 3", levels.get("Level 3", 0))
    c5.metric("Level 4", levels.get("Level 4", 0))

    st.divider()

    # ==========================================
    # Save All Papers
    # ==========================================

    if st.button("💾 Save All Results", use_container_width=True):
        saved_count = 0
        for paper in filtered_papers:
            result = save_paper(project_id=1, paper=paper)
            if result.get("saved", False):
                saved_count += 1
        st.success(f"{saved_count} papers saved successfully.")

    # ==========================================
    # Render Papers UI via Helper Component
    # ==========================================

    for idx, paper in enumerate(filtered_papers):
        render_paper_card(paper, idx)

    # ==========================================
    # Step Completed Status
    # ==========================================

    if st.session_state.get("literature_completed"):
        st.success("✅ Step 4 Completed")
